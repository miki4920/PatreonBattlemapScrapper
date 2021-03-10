import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import browser_cookie3 as cookies
import re

patreon_cookies = cookies.chrome()


def download_file(map_url):
    request = requests.get(map_url, cookies=patreon_cookies)
    with open(request.headers['content-disposition'] + ".zip", "wb") as file:
        file.write(request.content)



session = requests.Session()
session.get("https://www.patreon.com/czepeku", cookies=patreon_cookies)
request = str(session.get("""https://www.patreon.com/api/posts?include=campaign%2Caccess_rules%2Cattachments%2Caudio
%2Cimages%2Cmedia%2Cpoll.choices%2Cpoll.current_user_responses.user%2Cpoll.current_user_responses.choice%2Cpoll
.current_user_responses.poll%2Cuser%2Cuser_defined_tags&fields[
campaign]=currency%2Cshow_audio_post_download_links%2Cavatar_photo_url%2Cearnings_visibility%2Cis_nsfw%2Cis_monthly
%2Cname%2Curl&fields[post]=change_visibility_at%2Ccomment_count%2Ccontent%2Ccurrent_user_can_comment
%2Ccurrent_user_can_delete%2Ccurrent_user_can_view%2Ccurrent_user_has_liked%2Cembed%2Cimage%2Cis_paid%2Clike_count
%2Cmeta_image_url%2Cmin_cents_pledged_to_view%2Cpost_file%2Cpost_metadata%2Cpublished_at%2Cpatreon_url%2Cpost_type
%2Cpledge_url%2Cthumbnail_url%2Cteaser_text%2Ctitle%2Cupgrade_url%2Curl%2Cwas_posted_by_campaign_owner&fields[
post_tag]=tag_type%2Cvalue&fields[user]=image_url%2Cfull_name%2Curl&fields[
access_rule]=access_rule_type%2Camount_cents&fields[
media]=id%2Cimage_urls%2Cdownload_url%2Cmetadata%2Cfile_name&filter[campaign_id]=2318879&filter[
contains_exclusive_posts]=true&filter[is_draft]=false&sort=-published_at&json-api-version=1.0""",
                          cookies=patreon_cookies).content)
files = re.findall(r"<a href=\\\\\"(https:\/\/www\.patreon\.com\/file\?h=[0-9]+&amp;i=[0-9]+)\\\\\">[\w -]*\$5 Rewards", request)
for i in range(0, len(files)):
    files[i] = files[i].replace("amp;", "")

processes = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for url in files:
        processes.append(executor.submit(download_file, url))
