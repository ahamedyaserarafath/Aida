import feedparser
import webbrowser
from datetime import datetime , timedelta
from time import mktime
import html2text

class AtomFeeder():
    def __init__(self, atom_feeder_url,
                    delay_between_check_in_minutes = 5,
                    app_name = "app_name"):
        self.delay_between_check_in_minutes = delay_between_check_in_minutes
        self.app_name = app_name
        self.atom_feeder_url = atom_feeder_url
        self.incident_list = []

    def incident_check(self):
        try:
            now_utc = datetime.utcnow()
            utc_plus_delay_min = now_utc - timedelta(minutes=self.delay_between_check_in_minutes)
            app_feed = feedparser.parse(self.atom_feeder_url)
            app_feed_entries = app_feed.entries
            is_incident = False
            for entries in app_feed_entries:
                dt = datetime.fromtimestamp(mktime(entries.updated_parsed)).strftime("%Y-%m-%d %H:%M:%S")
                myDate = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S");
                # myDate = datetime.strptime("2021-06-01 13:08:39", "%Y-%m-%d %H:%M:%S");
                # if now_utc > myDate :
                if now_utc > myDate and myDate > utc_plus_delay_min:
                    print("Incident/update happened")
                    link = entries.link
                    unique_id = self.app_name + (entries.link).split("/")[-1]
                    summary = html2text.html2text(entries.summary)
                    title = entries.title
                    print(f"{unique_id} {summary}")
                    incident_dict = {
                        "link" : link,
                        "unique_id" : unique_id,
                        "title" : title,
                        "summary" : summary
                    }
                    self.incident_list.append(incident_dict)
            return self.incident_list
        except Exception as e:
            return "Exception occured while fetching the data : " + str(e)
