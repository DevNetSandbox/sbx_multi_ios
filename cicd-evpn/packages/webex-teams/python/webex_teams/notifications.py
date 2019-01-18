from webexteamssdk import WebexTeamsAPI


def send_webex_teams(token, room_id, changes):
    md = "**Network Change Detected**\n\n"
    for change in changes:
        keypath, op, oldval, newval = change
        line = "`{}` **Operation:** {} **Old Value:** {} **New Value:** {}\n\n"
        md += line.format(keypath, op, oldval, newval)

    api = WebexTeamsAPI(access_token=token)
    api.messages.create(room_id, markdown=md)
