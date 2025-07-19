This folder stores the original data files actually used by the web crawler, in their unprocessed form before any cleaning, parsing, or reformatting.

📌 Purpose
Preserve exactly what the crawler downloaded and used, such as Excel/CSV tables.

Provide a traceable source of truth for debugging, validation, or re-running the crawling pipeline.

Serve as the input source for all downstream data processing workflows.

🗂️ Typical File Types
mayor_url.xlsx — Raw mayor profile URLs

secretary_url.xlsx — Raw secretary profile URLs

🛠️ Usage Notes
Do not manually edit files in this folder. They should reflect exactly what was downloaded.

For cleaned or processed data, refer to the data/folder.