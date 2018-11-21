import pandas as pd
import ch1
from pathlib import Path
import os

a_db = ch1.IntoPostgres("postgres server entry data")
a_db.pcur(a_db.dbase, a_db.host, a_db.port, a_db.usern, a_db.pw)

t1 = "actual_termek"
t2 = "actual_ugynok"
t3 = "cikkszam"

t4 = "tcsop"

a_db.pX("DROP TABLE IF EXISTS " + t1 + " CASCADE;")
a_db.pX("DROP TABLE IF EXISTS " + t2 + " CASCADE;")
a_db.pX("DROP TABLE IF EXISTS " + t3 + " CASCADE;")
a_db.pX("DROP TABLE IF EXISTS " + t4 + " CASCADE;")

a_db.pX("CREATE TABLE "+ t1 +"(blank int, bizszam text, bizszam2 text, hova text, kiall_dat DATE, telj_dat DATE, esed_dat DATE, deviza text, targy text, netto decimal, afa decimal, brutto decimal, arfolyam decimal, sorsz int, cikkszam text, megnev text, ear decimal, ertek decimal, menny decimal, netto_ossz decimal, afa_ossz decimal, brutto_ossz decimal, filename text DEFAULT NULL);")
a_db.pX("CREATE TABLE "+ t2 +"(blank text, bizszam text, ugynok text, uzletag text, filename text DEFAULT NULL);")
a_db.pX("CREATE TABLE "+ t3 +"(blank text, cikkszam text, megnev text, csikkcsop1 text, csikkcsop2 text, besz_ar decimal, filename text DEFAULT NULL);")
a_db.pX("CREATE TABLE "+ t4 +"(blank text, cikkcsop1 text, tcsop text, filename text);")

print("drop and create basic tables")

                    ##copying the actual sold items per product datatables into postgres database
path1 = Path('/root/ch/1_Actual_termek/')
npath1 = Path('/root/ch/1_Actual_termek/CSV/')
columns1 = ['Bizonylatszám', 'Bizonylatszám 2.', 'Hová','Kiállítás', 'Teljesítés', 'Esedékes','Deviza', 'Tárgy', 'Nettó', 'Áfa', 'Bruttó', 'Árfolyam', 'S.sz.', 'Cikkszám', 'Megnevezés','Egységár', 'Érték', 'Mennyiség', 'Nettó összeg', 'ÁFA összeg', 'Bruttó összeg']
                    
a_db.excel_to_pg2(path1, npath1, t1, columns1)
a_db.pX("COMMIT;")
print("actual_termék COPY ok")
                    ##copying the actual salesperson per invoice datatables into postgres database
path2 = Path('/root/ch/2_Actual_ugynok/')
npath2 = Path('/root/ch/2_Actual_ugynok/CSV/')
columns2 = ['Bizonylatszám','Ügynök','Üzletág']
                
a_db.excel_to_pg2(path2, npath2, t2, columns2)
a_db.pX("COMMIT;")
print("actual_ügynök COPY ok")
                    ##copying the actual product datatables into postgres database
path3 = Path('/root/ch/3_Actual_cikkek/')
npath3 = Path('/root/ch/3_Actual_cikkek/CSV/')
columns3 = ['Cikkszám', 'Megnevezés 1.', 'Cikkcsoport (1.szint)', 'Cikkcsoport (2.szint)', 'Száll. besz. ár HUF']

a_db.excel_to_pg2(path3, npath3, t3, columns3)
a_db.pX("COMMIT;")
print("cikkszám COPY ok")


                    ##we copy the product group matching tables into the database.
path4 = Path('/root/ch/tcsop/')
npath4 = Path('/root/ch/tcsop/CSV/')
columns4 = ['cikkcsop1', 'ovont_kateg']

a_db.excel_to_pg2(path4, npath4, t4, columns4)
a_db.pX("COMMIT;")
print("tcsop COPY ok")

                    ##copying the so-called 'match-file' into postgres database -> the match-file matches the filenames of the actual sold items per product and the product datatables filenames into one file
                    # -> in order to be able to match the proper purchase-prices to the proper sold prices
path_at = Path('/root/ch/1_Actual_termek/')
path_c = Path('/root/ch/3_Actual_cikkek/')
at_fn = os.listdir(path_at)
c_fn = os.listdir(path_c)

a_db.pX("DROP TABLE IF EXISTS files_match CASCADE")
a_db.pX("CREATE TABLE files_match (blank text, act_fn text, cikk_fn text);")

full_fn = pd.DataFrame(
{'at_fn': at_fn,
'c_fn': c_fn
})

path_full_fn = Path('/root/ch/full_fn/')
filename = 'full_fn.csv'

full_fn.to_csv(path_full_fn / filename, sep=',', encoding='utf8')
fullfn_file = open(path_full_fn / filename, 'r', encoding='utf8')
a_db.cur.copy_expert("COPY files_match FROM STDIN WITH CSV HEADER ", fullfn_file)
a_db.pX("COMMIT;")
print("files_match COPY ok")

                ##PostgreSQL create databases
                #1. we drop the former tables with cascade
a_db.pX("DROP TABLE IF EXISTS act_t CASCADE;")
a_db.pX("DROP TABLE IF EXISTS act_t2 CASCADE;")

a_db.pX("DROP TABLE IF EXISTS cikktorzs_1 CASCADE;")
a_db.pX("DROP TABLE IF EXISTS cikktorzs_2 CASCADE;")
print("DROP TABLES act_t, act_t2, cikktorzs_1, cikktorzs_2 ok")

                #2. create and alter and update the basic tables
a_db.pX("CREATE TABLE act_t AS SELECT *, concat_ws('-', bizszam, sorsz) AS act_t_key, concat_ws('-', cikkszam, filename) AS cikk_fajl FROM actual_termek WHERE megnev not like '%előleg%' ORDER BY filename;")
print("create table act_t ok")
a_db.pX("CREATE TABLE act_t2 AS SELECT DISTINCT ON(act_t_key) act_t_key, blank, bizszam, bizszam2, hova, kiall_dat, telj_dat, esed_dat, deviza, targy, netto, afa, brutto, arfolyam, sorsz, cikkszam, megnev, ear, ertek, menny, (menny*ear*arfolyam) AS bev, netto_ossz, afa_ossz, brutto_ossz, filename, cikk_fajl FROM act_t ORDER BY act_t_key, filename;")
print("create table act_t2 ok")
a_db.pX("ALTER TABLE act_t2 ADD PRIMARY KEY (act_t_key);")
print("alter table act_t2 ok")
a_db.pX("CREATE TABLE cikktorzs_1 AS SELECT cikkszam.*, files_match.act_fn, concat_ws('-', cikkszam, files_match.act_fn) AS cikk_fajl, tcsop FROM cikkszam LEFT JOIN files_match ON cikkszam.filename=files_match.cikk_fn LEFT JOIN tcsop ON cikkszam.csikkcsop1=tcsop.cikkcsop1")
print("create table cikktorzs_1 ok")
a_db.pX("CREATE TABLE cikktorzs_2 AS SELECT DISTINCT ON(cikk_fajl) cikk_fajl, blank, cikkszam, megnev, csikkcsop1 as cikkcsop1, csikkcsop2 as cikkcsop2, besz_ar, tcsop, filename FROM cikktorzs_1;")
print("create table cikktorzs_2 ok")
a_db.pX("ALTER TABLE cikktorzs_2 ADD PRIMARY KEY (cikk_fajl);")
print("alter table cikktorzs_2 ok")
a_db.pX("UPDATE cikktorzs_2 SET tcsop = CASE WHEN cikkcsop1 like '°%IEC%' THEN 'IEC csoport' ELSE 'Egyéb' END WHERE tcsop is Null;")
print("UPDATE cikktorzs_2 ok")

                #3. we drop the tables originated from the basic tables and create them newly
a_db.pX("DROP TABLE IF EXISTS cikkt_3_dist CASCADE;")
a_db.pX("DROP TABLE IF EXISTS a_full_1 CASCADE;")
a_db.pX("DROP TABLE IF EXISTS a_full CASCADE;")
print("drop table cikkt_3_dist, a_full_1 és a_full ok")

a_db.pX("CREATE TABLE cikkt_3_dist AS SELECT DISTINCT ON(cikkszam) cikkszam, megnev, cikkcsop1, cikkcsop2, besz_ar, tcsop FROM cikktorzs_2;")
print("CREATE TABLE cikkt_3_dist ok")
a_db.pX("CREATE TABLE a_full_1 AS SELECT DISTINCT act_t2.*, cikktorzs_2.cikkcsop1, cikktorzs_2.cikkcsop2, cikktorzs_2.besz_ar, cikktorzs_2.megnev AS ct_megnev, cikktorzs_2.tcsop, actual_ugynok.ugynok, actual_ugynok.uzletag, cikkt_3_dist.besz_ar AS besz_ar2 FROM ((act_t2 LEFT JOIN cikktorzs_2 ON act_t2.cikk_fajl=cikktorzs_2.cikk_fajl) LEFT JOIN actual_ugynok ON  act_t2.bizszam=actual_ugynok.bizszam) LEFT JOIN cikkt_3_dist ON act_t2.cikkszam=cikkt_3_dist.cikkszam;")
print("CREATE TABLE a_full_1 ok")
a_db.pX("CREATE TABLE a_full AS SELECT *, EXTRACT(YEAR FROM telj_dat) AS ev, EXTRACT(MONTH FROM telj_dat) AS ho, CASE WHEN besz_ar IS NULL THEN besz_ar2 WHEN besz_ar IS NOT NULL THEN besz_ar END AS besz_ar_v FROM a_full_1;")
print("CREATE TABLE a_full ok")
a_db.pX("ALTER TABLE a_full ADD COLUMN ug_rov text;")
print("ALTER TABLE a_full1 ok")
a_db.pX("ALTER TABLE a_full ADD COLUMN tcs_rov text;")
print("ALTER TABLE a_full2 ok")

                #4. we create View-s from the originated tables
a_db.pX("CREATE VIEW ev_ho_arbev AS SELECT ev, ho, SUM(bev) AS bevetel FROM a_full GROUP BY ho, ev ORDER BY ev, ho;")
print("CREATE VIEW ev_ho_arbev ok")
a_db.pX("CREATE VIEW uzletagi_bev_ke AS SELECT ev, ho, SUM(bev) AS arbev FROM a_full WHERE uzletag='KE_div' GROUP BY ev, ho ORDER BY ev, ho;")
print("CREATE VIEW uzletagi_bev_ke ok")
a_db.pX("CREATE VIEW uzletagi_bev_hm AS SELECT ev, ho, SUM(bev) AS arbev FROM a_full WHERE uzletag='HM_div' GROUP BY ev, ho ORDER BY ev, ho;")
print("CREATE VIEW uzletagi_bev_hm ok")
a_db.pX("CREATE VIEW bev_fed AS SELECT ev, ho, SUM(bev) AS arbev, SUM(menny*besz_ar_v) AS ktg FROM a_full GROUP BY ev, ho ORDER BY ev, ho;")
print("CREATE VIEW bev_fed ok")
a_db.pX("CREATE VIEW hm_bev_fed AS SELECT ev, ho, SUM(bev) AS arbev, SUM(menny*besz_ar_v) AS ktg FROM a_full WHERE uzletag='HM_div' GROUP BY ev, ho ORDER BY ev, ho;")
print("CREATE VIEW hm_bev_fed ok")
a_db.pX("CREATE VIEW ke_bev_fed AS SELECT ev, ho, SUM(bev) AS arbev, SUM(menny*besz_ar_v) AS ktg FROM a_full WHERE uzletag='KE_div' GROUP BY ev, ho ORDER BY ev, ho;")
print("CREATE VIEW ke_bev_fed ok")
a_db.pX("CREATE VIEW hm_ev_ua_ho_ug AS SELECT ev, uzletag, ho, ug_rov, sum(menny*ear*arfolyam/1000) as arbev, sum(menny*besz_ar_v/1000) as ktg  FROM a_full WHERE uzletag='HM_div' GROUP BY uzletag, ev, ho, ug_rov ORDER BY ev, uzletag, ho, arbev DESC;")
print("CREATE VIEW hm_ev_ua_ho_ug ok")
a_db.pX("CREATE VIEW ke_ev_ua_ho_ug AS SELECT ev, uzletag, ho, ug_rov, sum(menny*ear*arfolyam/1000) as arbev, sum(menny*besz_ar_v/1000) as ktg  FROM a_full WHERE uzletag='KE_div' GROUP BY uzletag, ev, ho, ug_rov ORDER BY ev, uzletag, ho, arbev DESC;")
print("CREATE VIEW ke_ev_ua_ho_ug ok")
a_db.pX("CREATE VIEW tcsop_hm_18 AS SELECT tcs_rov, SUM(menny*ear*arfolyam)/1000000 AS bev, SUM(menny*besz_ar_v)/1000000 AS ktg FROM a_full WHERE ev='2018' AND megnev not like '%előleg%' AND uzletag='HM_div' AND tcsop not like '%Előleg%' AND tcsop not like '%KE_divGÉPEK%' GROUP BY tcs_rov ORDER BY bev DESC;")
a_db.pX("CREATE VIEW tcsop_hm_17 AS SELECT tcs_rov, SUM(menny*ear*arfolyam)/1000000 AS bev, SUM(menny*besz_ar_v)/1000000 AS ktg FROM a_full WHERE ev='2017' AND megnev not like '%előleg%' AND uzletag='HM_div' AND tcsop not like '%Előleg%' AND tcsop not like '%KE_divGÉPEK%' GROUP BY tcs_rov ORDER BY bev DESC;")
print("CREATE VIEW tcsop_hm ok")
a_db.pX("CREATE VIEW hm_tcsop_ho_18 AS SELECT tcs_rov, ho, SUM(menny*ear*arfolyam) AS bev, SUM(menny*besz_ar_v) AS ktg, SUM(menny*ear*arfolyam-menny*besz_ar_v) AS fed FROM a_full WHERE uzletag='HM_div' AND ev='2018' GROUP BY tcs_rov, ho ORDER BY ho ASC;")
print("CREATE VIEW hm_tcsop_ho_18 ok")
a_db.pX("CREATE VIEW hm_tcsop_ho_17 AS SELECT tcs_rov, ho, SUM(menny*ear*arfolyam) AS bev, SUM(menny*besz_ar_v) AS ktg, SUM(menny*ear*arfolyam-menny*besz_ar_v) AS fed FROM a_full WHERE uzletag='HM_div' AND ev='2017' GROUP BY tcs_rov, ho ORDER BY ho ASC;")
print("CREATE VIEW hm_tcsop_ho_17 ok")

print("EVERYTHING OK!!!!!")

a_db.pX("COMMIT;")

