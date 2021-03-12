import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import browser_cookie3 as cookies
import re
import json

patreon_cookies = cookies.chrome()
starting_url = """https://www.patreon.com/api/posts?include=campaign%2Caccess_rules%2Cattachments%2Caudio%2Cimages
%2Cmedia%2Cpoll.choices%2Cpoll.current_user_responses.user%2Cpoll.current_user_responses.choice%2Cpoll
.current_user_responses.poll%2Cuser%2Cuser_defined_tags&fields[
campaign]=currency%2Cshow_audio_post_download_links%2Cavatar_photo_url%2Cearnings_visibility%2Cis_nsfw%2Cis_monthly
%2Cname%2Curl&fields[post]=change_visibility_at%2Ccomment_count%2Ccontent%2Ccurrent_user_can_comment
%2Ccurrent_user_can_delete%2Ccurrent_user_can_view%2Ccurrent_user_has_liked%2Cembed%2Cimage%2Cis_paid%2Clike_count
%2Cmeta_image_url%2Cmin_cents_pledged_to_view%2Cpost_file%2Cpost_metadata%2Cpublished_at%2Cpatreon_url%2Cpost_type
%2Cpledge_url%2Cthumbnail_url%2Cteaser_text%2Ctitle%2Cupgrade_url%2Curl%2Cwas_posted_by_campaign_owner&fields[
post_tag]=tag_type%2Cvalue&fields[user]=image_url%2Cfull_name%2Curl&fields[
access_rule]=access_rule_type%2Camount_cents&fields[
media]=id%2Cimage_urls%2Cdownload_url%2Cmetadata%2Cfile_name&filter[campaign_id]=2318879&filter[
contains_exclusive_posts]=true&filter[is_draft]=false&sort=-published_at&page[
cursor]=R5W0_BFScqCs7v-BifthA1Kjpco&json-api-version=1.0 """


def download_file(map_url):
    request = requests.get(map_url, cookies=patreon_cookies, stream=True)
    name = re.search(r"filename=\"([\w \[\]\-\$\.]*)\";", request.headers['content-disposition']).group(1)
    total_length = request.headers.get('content-length')
    dl = 0
    count = 0
    total_length = int(total_length)
    with open("maps/" + name, "wb") as file:
        for data in request.iter_content(chunk_size=4096):
            dl += len(data)
            file.write(data)
            done = int(50 * dl / total_length)
            if done > count:
                count = done
                print("[%s%s]" % ('=' * done, ' ' * (50 - done)))


session = requests.Session()
request = session.get(starting_url, cookies=patreon_cookies)
download_file_list = []
while True:
    content = str(request.content)
    files = re.findall(
        r"<a href=\\\\\"(https:\/\/www\.patreon\.com\/file\?h=[0-9]+&amp;i=[0-9]+)\\\\\">[\w -]*\$5 Rewards", content)
    download_file_list.extend(files)
    next_url = request.json().get("links")
    if next_url:
        next_url = next_url["next"]
        request = session.get(next_url, cookies=patreon_cookies)
    else:
        break

for i in range(0, len(download_file_list)):
    download_file_list[i] = download_file_list[i].replace("amp;", "")

processes = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for url in download_file_list:
        processes.append(executor.submit(download_file, url))
