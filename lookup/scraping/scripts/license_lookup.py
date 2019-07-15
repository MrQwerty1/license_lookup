import argparse
import itertools
import json
import requests

from lxml import html


def __init():
    r = requests.get('https://red.prod.secure.nv.gov/Lookup/LicenseLookup.aspx')
    tree = html.fromstring(r.text)
    st = tree.xpath("//select[@id='MainContentPlaceHolder_ucLicenseLookup_ctl01_ddStates']/option[@value!='']")
    states = {}
    for s in st:
        name = s.xpath("./text()")[0].lower()
        value = s.xpath("./@value")[0]
        states[name] = value

    data_part = {
        '__VIEWSTATE': tree.xpath("//input[@name='__VIEWSTATE']/@value")[0],
        '__VIEWSTATEGENERATOR': tree.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value")[0]
    }

    return data_part, states


def get_county(state, county):
    data = {'state': state}
    r = requests.post('https://red.prod.secure.nv.gov/AjaxWebServices/CommonService.svc/GetCountiesByState', json=data)
    li = r.json()["d"]
    li = list(map(str.lower, li))
    li.reverse()
    counties = dict(itertools.zip_longest(*[iter(li)] * 2, fillvalue=""))
    return counties[county]


def run(fname, lname, state, county, cont_id):
    data_part, states = __init()

    if state != '':
        state = states[state]

        if county != '':
            county = get_county(state, county)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MicrosoftAjax': 'Delta=true',
    }

    data = {
        'ctl00$ScriptManager1': 'ctl00$MainContentPlaceHolder$ucLicenseLookup$UpdtPanelGridLookup|ctl00$MainContentPlaceHolder$ucLicenseLookup$UpdtPanelGridLookup',
        '__EVENTTARGET': 'ctl00$MainContentPlaceHolder$ucLicenseLookup$UpdtPanelGridLookup',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$ddCredPrefix': '',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$tbLicenseNumber': '',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$ddSubCategory': '',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$tbDBA_Contact': '',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$tbFirstName_Contact': fname,
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$tbLastName_Contact': lname,
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$tbCity_ContactAddress': '',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$ddStates': state,
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$tbZipCode_ContactAddress': '',
        'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl01$ddCounty': county,
        '__ASYNCPOST': True,
    }
    data.update(data_part)

    r = requests.post('https://red.prod.secure.nv.gov/Lookup/LicenseLookup.aspx', headers=headers, data=data)
    tree = html.fromstring(r.text)
    try:
        t = tree.xpath("//table[@id='MainContentPlaceHolder_ucLicenseLookup_gvSearchResults']//tr[./td[text()='ACTIVE']]")[0]
        out = {
            'Name': ''.join(t.xpath("./td[2]/text()")),
            'License Number': ''.join(t.xpath("./td[3]/text()")),
            'License Type': ''.join(t.xpath("./td[4]/text()")),
            'License Status': ''.join(t.xpath("./td[5]/text()")),
            'City': ''.join(t.xpath("./td[6]/text()")),
            'State': ''.join(t.xpath("./td[7]/text()")),
            'Zip Code': ''.join(t.xpath("./td[8]/text()")),
            'Cont_id': cont_id
        }
        return out
    except:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('first_name_p')
    parser.add_argument('last_name_p')
    parser.add_argument('state_p')
    parser.add_argument('county_p')
    parser.add_argument('cont_id')
    args = parser.parse_args()
    fname = args.first_name_p
    lname = args.last_name_p
    state = args.state_p.lower()
    county = args.county_p.lower()
    cont_id = args.cont_id
    js = run(fname, lname, state, county, cont_id)
    print(js)
