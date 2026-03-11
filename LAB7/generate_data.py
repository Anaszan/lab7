import csv
import re
import os

raw_data_text = """1	1800	4.2	1.2	1	0.72	Arabica Premium
2	600	6.1	2.7	3	1.05	Robusta Commercial
3	1100	5.5	1.8	2	0.88	Liberica Rare
4	1500	4.8	1.4	1	0.75	Excelsa Bold
5	2100	3.9	1.1	1	0.69	Arabica Premium
6	450	6.5	3.1	3	1.10	Robusta Commercial
7	950	5.2	2.0	2	0.91	Liberica Rare
8	1650	4.5	1.3	2	0.78	Arabica Premium
9	700	6.3	2.9	3	1.08	Robusta Commercial
10	1400	5.0	1.6	1	0.80	Excelsa Bold
11	2000	4.0	1.0	1	0.68	Arabica Premium
12	550	6.4	3.0	3	1.09	Robusta Commercial
13	1200	5.3	1.9	2	0.89	Liberica Rare
14	1550	4.7	1.5	1	0.77	Excelsa Bold
15	1900	4.1	1.1	1	0.70	Arabica Premium
16	500	6.6	3.2	3	1.11	Robusta Commercial
17	1050	5.4	2.1	2	0.90	Liberica Rare
18	1700	4.4	1.2	2	0.74	Arabica Premium
19	650	6.2	2.8	3	1.07	Robusta Commercial
20	1350	4.9	1.7	1	0.81	Excelsa Bold
21	2200	3.8	1.0	1	0.67	Arabica Premium
22	400	6.7	3.3	3	1.12	Robusta Commercial
23	1150	5.6	2.2	2	0.92	Liberica Rare
24	1450	4.6	1.4	1	0.76	Excelsa Bold
25	2050	4.1	1.1	1	0.69	Arabica Premium
26	480	6.5	3.0	3	1.10	Robusta Commercial
27	980	5.3	2.0	2	0.90	Liberica Rare
28	1600	4.5	1.3	2	0.77	Arabica Premium
29	720	6.3	2.9	3	1.08	Robusta Commercial
30	1380	5.0	1.6	1	0.80	Excelsa Bold
31	1850	4.2	1.2	1	0.71	Arabica Premium
32	580	6.4	3.1	3	1.09	Robusta Commercial
33	1080	5.1	1.8	2	0.87	Liberica Rare
34	1520	4.8	1.5	1	0.78	Excelsa Bold
35	2150	3.9	1.0	1	0.68	Arabica Premium
36	420	6.6	3.2	3	1.11	Robusta Commercial
37	1020	5.4	2.1	2	0.91	Liberica Rare
38	1720	4.3	1.2	1	0.73	Arabica Premium
39	660	6.2	2.8	3	1.07	Robusta Commercial
40	1420	4.9	1.7	1	0.82	Excelsa Bold
41	1950	4.0	1.1	1	0.70	Arabica Premium
42	530	6.5	3.0	3	1.10	Robusta Commercial
43	1130	5.5	2.2	2	0.93	Liberica Rare
44	1480	4.7	1.4	1	0.76	Excelsa Bold
45	2080	4.1	1.1	1	0.69	Arabica Premium
46	460	6.7	3.3	3	1.12	Robusta Commercial
47	1000	5.2	1.9	2	0.89	Liberica Rare
48	1580	4.6	1.3	2	0.76	Arabica Premium
49	680	6.3	2.9	3	1.08	Robusta Commercial
50	1360	5.0	1.6	1	0.81	Excelsa Bold
51	1820	4.2	1.2	1	0.72	Arabica Premium
52	560	6.4	3.1	3	1.09	Robusta Commercial
53	1060	5.3	2.0	2	0.90	Liberica Rare
54	1540	4.8	1.5	1	0.79	Excelsa Bold
55	2120	3.9	1.0	1	0.67	Arabica Premium
56	510	6.6	3.2	3	1.11	Robusta Commercial
57	1040	5.4	2.1	2	0.91	Liberica Rare
58	1680	4.4	1.2	1	0.74	Arabica Premium
59	630	6.2	2.8	3	1.06	Robusta Commercial
60	1390	4.9	1.7	1	0.83	Excelsa Bold
61	1870	4.1	1.1	1	0.70	Arabica Premium
62	440	6.7	3.3	3	1.13	Robusta Commercial
63	1170	5.6	2.3	2	0.93	Liberica Rare
64	1460	4.6	1.4	1	0.75	Excelsa Bold
65	2030	4.0	1.1	1	0.68	Arabica Premium
66	490	6.5	3.0	3	1.10	Robusta Commercial
67	990	5.2	2.0	2	0.88	Liberica Rare
68	1630	4.5	1.3	2	0.77	Arabica Premium
69	710	6.3	2.9	3	1.08	Robusta Commercial
70	1410	5.0	1.6	1	0.80	Excelsa Bold
71	2250	3.8	1.0	1	0.66	Arabica Premium
72	390	6.8	3.4	3	1.14	Robusta Commercial
73	1190	5.5	2.2	2	0.92	Liberica Rare
74	1490	4.7	1.5	1	0.77	Excelsa Bold
75	1980	4.0	1.1	1	0.69	Arabica Premium
76	570	6.4	3.1	3	1.09	Robusta Commercial
77	1070	5.3	2.0	2	0.90	Liberica Rare
78	1560	4.6	1.3	2	0.76	Arabica Premium
79	640	6.2	2.8	3	1.07	Robusta Commercial
80	1430	4.9	1.7	1	0.82	Excelsa Bold
81	2180	3.9	1.0	1	0.67	Arabica Premium
82	410	6.6	3.2	3	1.12	Robusta Commercial
83	1120	5.5	2.1	2	0.91	Liberica Rare
84	1510	4.8	1.4	1	0.78	Excelsa Bold
85	1910	4.1	1.1	1	0.70	Arabica Premium
86	475	6.5	3.0	3	1.10	Robusta Commercial
87	1015	5.3	1.9	2	0.89	Liberica Rare
88	1745	4.4	1.2	2	0.73	Arabica Premium
89	695	6.3	2.9	3	1.07	Robusta Commercial
90	1365	5.0	1.6	1	0.80	Excelsa Bold
91	2070	4.0	1.1	1	0.68	Arabica Premium
92	520	6.6	3.1	3	1.11	Robusta Commercial
93	1145	5.4	2.2	2	0.92	Liberica Rare
94	1475	4.7	1.4	1	0.76	Excelsa Bold
95	1835	4.2	1.2	1	0.71	Arabica Premium
96	545	6.5	3.0	3	1.10	Robusta Commercial
97	1035	5.2	2.0	2	0.89	Liberica Rare
98	1615	4.5	1.3	1	0.77	Arabica Premium
99	675	6.3	2.8	3	1.06	Robusta Commercial
100	1395	4.9	1.7	1	0.81	Excelsa Bold"""

rows = []
for line in raw_data_text.strip().split('\n'):
    parts = re.split(r'\t', line)
    if len(parts) >= 7:
        rows.append(parts[1:])

with open('coffee_beans.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Altitude', 'Acidity', 'Caffeine_Content', 'Roast_Level', 'Density', 'Species'])
    for r in rows:
        writer.writerow(r)

print("Generated coffee_beans.csv successfully.")
