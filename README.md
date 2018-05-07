# apple-status-api
Publish Apple service status notifications as a simple REST API

To deploy:

- Install chalice with `pip install chalice`
- Make sure to follow AWS setup instructions for chalice at [http://chalice.readthedocs.io/en/latest/]()
- Clone this repository
- `cd apple-status-api`
- To run a local instance of the app:
- `chalice local`
- To run a dev instance on AWS (assuming AWS credentials have been configured):
- `chalice deploy --stage dev` (optionally use --profile if you have multiple AWS profiles)
- To run a production instance on AWS:
- `chalice deploy --stage prod` (again optionally using --profile if required)

## Example use

These are some of the endpoints currently implemented, all responses are JSON.

Get list of all currently tracked service both from the main Apple status page and the Developer status page:

`curl https://aws-node/api/services`

Response:

`["App Store", "Apple ID", "Apple Music", "Apple Music Subscriptions", "Apple Online Store", "Apple Pay", "Apple School Manager", "Apple TV", "Back to My Mac", "Beats 1", "Device Enrollment Program", "Dictation", "Documents in the Cloud", "FaceTime", "Find My Friends", "Find My iPhone", "Game Center", "iBooks Store", "iCloud Account & Sign In", "iCloud Backup", "iCloud Bookmarks & Tabs", "iCloud Calendar", "iCloud Contacts", "iCloud Drive", "iCloud Keychain", "iCloud Mail", "iCloud Notes", "iCloud Reminders", "iCloud Storage Upgrades", "iCloud Web Apps (iCloud.com)", "iMessage", "iOS Device Activation", "iTunes in the Cloud", "iTunes Match", "iTunes Store", "iTunes U", "iWork for iCloud", "Mac App Store", "macOS Software Update", "Mail Drop", "Maps Display", "Maps Routing & Navigation", "Maps Search", "Maps Traffic", "News", "Photo Print Products", "Photos", "Radio", "Siri", "Spotlight suggestions", "Volume Purchase Program", "Account", "APNS", "APNS Sandbox", "Apple Developer Forums", "Apple Music API", "Apple News API", "Apple Pay", "Bug Reporter", "Certificates, Identifiers & Profiles", "CloudKit Dashboard", "Code-level Support", "Contact Us", "Developer Documentation", "In-App Purchases", "iTunes Connect", "iTunes Sandbox", "News Publisher", "Program Enrollment and Renewals", "Software Downloads", "TestFlight", "Videos", "Xcode Automatic Configuration"]`

---

Get current complete status report about a service (as provided by Apple):

`curl https://aws-node/api/service/Device%20Enrollment%20Program` (note URL escaping, some services have spaces in their names)

Response:

`{"redirectUrl": null, "serviceName": "Device Enrollment Program", "events": [{"usersAffected": "All users were affected", "endDate": "05/05/2018 15:00 PDT", "startDate": "05/05/2018 03:00 PDT", "epochStartDate": 1525514400000, "datePosted": "05/07/2018 01:00 PDT", "eventStatus": "completed", "epochEndDate": 1525557600000, "messageId": "2141", "affectedServices": null, "message": "Due to system maintenance, recently purchased devices may have experience delayed enrollments", "statusType": "Maintenance"}]}`

Or:

`curl https://aws-node/api/service/iTunes`

Response:

`{"redirectUrl": null, "serviceName": "iTunes Sandbox", "events": []}`

---

Get simple up/down status for the service (boolean):

`curl https://aws-node/api/service/Device%20Enrollment%20Program/up`

Response:

`true`

---

Get status report for all Developer services:

`curl https://aws-node/api/devstatus`

Get status report for all regular services:

`curl https://aws-node/api/prodstatus`
