import random
import streamlit as st
rate4 = .052
rate5 = .006
rate5pity = 0.0645

def pull(pity4, pity5):
  if pity5 == 89: return 5
  if pity4 == 9: return 4
  r = random.uniform(0,1)
  if pity5 > 74:
    if r < rate5pity: return 5
    if r < rate5pity + rate4: return 4
    return 0
  if r < rate5: return 5
  if r < rate5 + rate4: return 4
  return 0

pulls = st.sidebar.number_input('Number of pulls to simulate:', min_value = 0, max_value = 10000)
saved_pity_5 = st.sidebar.number_input('Existing 5* pity:', min_value = 0, max_value = 89, value = 0)
saved_pity_4 = st.sidebar.number_input('Existing 4* pity:', min_value = 0, max_value = 10, value = 0)
guaranteed = st.sidebar.selectbox('50/50 guarantee:', [False, True])

if st.sidebar.button('Run simulation!'):

  iterations = 10000
  totals = {0:0, 4:0, 5:0, '5*':0}

  for _ in range(iterations):
    pity4 = saved_pity_4
    pity5 = saved_pity_5
    results = {}
    results[0] = 0
    results[4] = 0
    results[5] = 0
    results["5*"] = 0
    fifty = guaranteed
    for i in range(pulls):
      out = pull(pity4, pity5)
      pity4 += 1
      pity5 += 1
      if out == 4: 
        pity4 = 0
        results[4] += 1
      if out == 5:
        if fifty or random.uniform(0, 1) >= .5:
          results["5*"] += 1
          fifty = False
        else:
          results[5] += 1
          fifty = True
        pity5 = 0
      if out == 0:
        results[0] +=1
    # Put success condition here
    totals[0] += results[0]
    totals[4] += results[4]
    totals[5] += results[5]
    totals['5*'] += results['5*']
  st.write(f'Expected number of on-banner 5*s: {totals["5*"] * 1.0/iterations:.2f}')
  st.write(f'Expected number of off-banner 5*s: {totals[5] * 1.0/iterations.2f}')
  st.write(f'Expected number of 4*s: {totals[4] * 1.0/iterations.2f}')
  st.write(f'Expected number of 3*s: {totals[0] * 1.0/iterations.2f}')
