import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from pytz import timezone

tz = timezone('EST')
states = ["alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware","district-of-columbia","florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico","new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania","rhode-island","south-carolina","south-dakota","tennessee","texas","utah","vermont","virginia","washington","west-virginia","wisconsin","wyoming"]
table = []
totals = []
pcts = []
remaining = []

for state in states:
  print('\r'+state, end='')
  source = requests.get('https://www.nytimes.com/interactive/2020/11/03/us/elections/results-'+state+'.html').text
  soup = BeautifulSoup(source, 'html.parser')
  prestable = soup.find(id='jump-president')
  totalvotetable = prestable.find('tr', class_='e-total-reported')
  total = int(totalvotetable.find('span', class_='e-votes-display').text.replace(',',''))
  pct = soup.find('p', class_='e-subhed').text[:2]
  if pct == 'Ne':
    pct = '100'
  pct = int(pct)
  table.append([state,total,pct])
  totals.append(total)
  pcts.append(pct)
  rem = round(total/pct*(100-pct))
  remaining.append(rem)
  print('\r'+'                              ', end='')
print('')

table.append(["TOTAL",sum(totals),round(100-100*sum(remaining)/sum(totals)),sum(remaining)])
totals.append(sum(totals))
remaining.append(sum(remaining))
pcts.append(round(100-100*remaining[51]/totals[51],1))
dispstates = states
dispstates.append("TOTALS")
fulltable = {"State":dispstates,"Total Votes":totals,"Percent Counted":pcts,"Remaining Ballots":remaining}
df = pd.DataFrame(fulltable)
df = df.set_index("State")
print(df)

time = datetime.now(tz).strftime('%m-%d-%H-%M')
filetime = 'electiondata_'+time+'.csv'
df.to_csv(filetime)