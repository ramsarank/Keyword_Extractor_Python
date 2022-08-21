"""
@author: Ram Saran K
"""

# Basic libraries 
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

# Import the data that needs the key word extraction to be performed on
data = pd.read_csv('InputData.csv')

# Pick the text column and perform cleaning -- such as lower, replace carriage returns, colons and etc
data['Description'] = data['desc_summary']
data['Description'] = data['Description'].astype(str)
data['Description'] = data['Description'].str.replace('\\r', ' ')
data['Description'] = data['Description'].str.replace('\\n', ' ')
data['Description'] = data['Description'].str.lower()
data['Description'] = data['Description'].str.replace('[^0-9a-zA-Zs:]+', ' ')
data['Description'] = data['Description'].str.replace('[[d]+%]+', ' ')
data['Description'] = data['Description'].str.replace('d[d\\.\\-]*d', ' ')
data['Description'] = data['Description'].str.replace('[Hh]ttp[s]{0,1}://[A-Za-z0-9./-]+', ' ')
data['Description'] = data['Description'].str.replace(':', ' ')


def check_keywords(data, words):
    wlist_regex = '\\b|\\b'.join(words)
    wlist_regex = '\\b' + wlist_regex
    wlist_regex = wlist_regex + '\\b'
    i = 0
    cnt = 0
    length = len(data.split())
    data_list = data.split()
    while i < length:
        cnt = len(set(re.findall(wlist_regex, ' '.join(data_list[i:i + 7]))))
        if cnt == len(words):
            return True
        elif cnt > 0 and cnt < len(words):
            i += 1
        else:
            i += 7
    return False
 


def update(data, word_lists, is_name):
    for wlist in word_lists:
        if check_keywords(data, wlist):
            return is_name
    return ''
  
  
# New column 
data['Level1'] = ''

# Extraction Conditions
data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(lambda x: update(x, [
    ['dropped', 'call'], ['lost', 'call'], ['noone', 'on', 'call'], ['call', 'dropped'], ['abandoned', 'call'],
    ['call', 'drop'], ['drop', 'call']], 'Abandoned/Drop call'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(
    lambda x: update(x, [['aborted', 'job'], ['aborted', 'jobs']], 'Aborted Jobs'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(lambda x: update(x, [
    ['abend', 'job'], ['abended', 'job'], ['job', 'abend'], ['job', 'abended'], ['jobs', 'abend'], ['jobs', 'abended']], 'Abended Jobs'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(
    lambda x: update(x, [['ac', 'propulsion']], 'AC Propulsion Issue'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(
    lambda x: update(x, [['antivirus', 'issue'], ['anti', 'virus', 'issue']], 'AV Related'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(lambda x: update(x, [
    ['rebooting'], ['reboot'], ['booting', 'issue'], ['not', 'booting'], ['not', 'boot'], ['reboots'],
    ['will', 'not', 'boot'], ['wont', 'boot'], ['nt', 'has', 'been', 'rebooted '], ['node', 'reboot'],
    ['node', 'rebooted']], 'Boot/reboot'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(
    lambda x: update(x, [['windows', 'event', 'log']], 'Windows Event Log'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(
    lambda x: update(x, [['wrong', 'hd'], ['wrong', 'help'], ['trans', 'epims']], 'Wrong Helpdesk'))

data.loc[data['Level1'] == '', 'Level1'] = data[data['Level1'] == ''].Description.map(
    lambda x: update(x, [['number', 'zombie', 'excessive'], ['zombie'], ['zombie', 'process', 'state']],
                     'Zombie Process'))


# Rest of the categories in to "Others"
data.loc[data['Level1'] == '', 'Level1'] = 'Others'

# Output the file with the keywords/categories extracted
data.to_csv('Output.csv')
