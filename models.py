release-example-json = {
"name": "<Your Repo’s Name>",
"category": [],
"suite": "stable",
"Version": 1,
"author": "name of author",
"description": "description",
"install_msg": "thank you for installing this repo",
"agreement": "To install this you agree to..." # leave "" for none
}

info-example-json = {
    "author": ["author of cog"],
    "install_msg": "Thanks for installing etc.",
    "files":["example.py"],
    "lib":["example.json"],
    "name": "name of cog",
    "disabled": false, # is cog disabled
    "short": "short description",
    "description": "long description",
    "tags": [],
    "requirements": ["example", "pip"], # pip installs
    "hidden": false, # is cog hidden
    "end_user_data_statement": "This cog does not store any End User Data." # privacy statement leave "" for none
}

packages-example-json = {
"reponame": "example",
"packagetotal": 1
"packagename": "/pathtopackage/",
"example": "/example/"
}
