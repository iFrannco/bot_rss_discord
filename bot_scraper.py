from functions import parse_and_upload_to_db, list_suscriptions

rss_list = list_suscriptions()
parse_and_upload_to_db(rss_list)

