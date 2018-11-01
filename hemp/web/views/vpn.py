from flask import render_template, request, flash, redirect, url_for

if __name__ == '__main__':
    if __package__ is None:
        sys.path.append(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
from services import nso

def vpn_list():
    return render_template('vpn-list.html')

def add_vpn():
    if request.method == "POST":
        # here we will accept the form data or apply reasonable defaults
        vpn_data = dict()
        vpn_data['partner_name'] = request.form.get("partner_name")
        vpn_data['sequence'] = request.form.get("sequence")
        vpn_data['peer_ip'] = request.form.get("peer_ip")
        vpn_data['isakmp_algo'] = request.form.get("isakmp_algo", "aes")
        vpn_data['isakmp_group'] = request.form.get("isakmp_group", "2")
        vpn_data['pre_shared_key'] = request.form.get("pre_shared_key")
        vpn_data['acl_number'] = request.form.get("acl_number")
        vpn_data['acl_rule'] = request.form.get("acl_rule")
        vpn_data['transform_auth'] = request.form.get("transform_auth")
        vpn_data['transform_encryption'] = request.form.get("transform_encryption")
        resp, payload =  nso.add_vpn(**vpn_data)
        if resp.ok:
            flash("Successfully Created VPN", 'success')
            return redirect(url_for('vpn-list'))
        else:
            return render_template('add-vpn-failure.html',
                                   vpn_data=payload,
                                   response=resp)

    else:
        return render_template('add-vpn.html')

def vpn_detail(partner_name):
    data = nso.get_vpn_details(partner_name)
    return render_template('vpn-detail.html', vpn=data)
