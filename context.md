Norwegian Endurance Athlete ECG Database

Abstract
The Norwegian Endurance Athlete ECG Database contains 12-lead ECG recordings from 28 elite athletes from various sports in Norway. All recordings are 10 seconds resting ECGs recorded with a General Electric (GE) MAC VUE 360 electrocardiograph. All ECGs are interpreted with both the GE Marquette SL12 algorithm (version 23 (v243)) and one cardiologist with training in interpretation of athlete's ECG. The data was collected at the University of Oslo in February and March 2020.

Background
Athletes often have increased thickness in the left ventricular wall and extended chambers in both the left and right ventricle compared to untrained people at the same age [1]. These changes occur as a result of the heart adapting to large amounts of exercise. These changes can be seen on an echocardiogram, but the changes also give electrical manifestations that can be observed on an electrocardiogram (ECG). Even if these changes are considered healthy, they can be confused with pathological changes that are related to sudden cardiac death (SCD) [2]. In addition, studies show that the incidence of SCD is higher in athletes than in non-athletes of the same age [3,4]. Current measures and procedures for detecting athletes with an increased risk of SCD are characterized by low accuracy and low precision. This emphasizes that ECG interpretation of athletes is an area that requires increased focus.

Methods
Twenty-eight healthy athletes were recruited for this study. 19 (68%) of the participants were men and 9 (32%) were women. Participant's ages ranged from 20 to 43 years (Mean = 25 years, standard deviation = 4.7 years). The distribution among sports was 24 rowers (86%), 2 kayakers (7%) and 2 cyclists (7%). The average amount of training hours for 2017 was 822 hours with a standard deviation of 117 hours, in 2018 the average amount of training was 820 hours with a standard deviation of 113 hours and in 2019 the average amount of training was 798 hours with a standard deviation of 171 hours.

The study protocol and consent form were approved by the Norwegian Centre for Research Data (application ID: 389013) and the University of Oslo, and the ethical considerations were approved by the Regional Committees for Medical and Health Research Ethics (application ID: 51205).  All participants were informed and gave written consent before the test was initiated, they also agreed to have their ECG shared in an open database after the project was finished. The test subjects were lying horizontally on a bed, relaxing, while electrodes were attached to perform a 12-lead ECG recording. The recordings were performed as a standard 10 seconds resting ECG. The device used was a GE MAC VUE 360. The device's built-in interpretation algorithm, Marquette 12SL (version 23 (v243)), performed automatic interpretation of all ECGs.

All ECG recordings were examined by a cardiologist, with specialization in athletes' hearts, after the recordings were completed. The cardiologist interpreted the ECGs according to the international criteria for ECG interpretation of athletes.

Data Description
Each of the 28 waveform files consists of 12 arrays, representing the twelve leads. The ECGs were obtained using a General Electric (GE) MAC VUE 360 electrocardiograph and interpreted using the built-in ECGs are GE Marquette SL12 algorithm (version 23 (v243)) and a cardiologist with training in interpretation of athlete's ECG.

The waveform files are stored in .dat -files with a corresponding .hea file containing all the metadata. This file formats are compatible with the Python WaveForm DataBase (WFDB) package and this makes it easy to import the data.

All ECG waveforms are sampled and stored with a sampling frequency of 500Hz and a length of 5000 samples (10 seconds). The header file contains information about the total amount of leads, samples per lead and additional information about each lead. The last two lines in the header file contains the diagnose given by the Marquette SL12 (SL12) algorithm and the cardiologist (C).


th_001 12 500 5000
ath_001.dat 16 50000/mV 16 0 10251 49595 0 I
ath_001.dat 16 50000/mV 16 0 -1096 35223 0 II
ath_001.dat 16 50000/mV 16 0 -10267 60826 0 III
ath_001.dat 16 50000/mV 16 0 -3724 3505 0 AVR
ath_001.dat 16 50000/mV 16 0 9391 26379 0 AVL
ath_001.dat 16 50000/mV 16 0 -5395 57481 0 AVF
ath_001.dat 16 50000/mV 16 0 13580 61759 0 V1
ath_001.dat 16 50000/mV 16 0 11410 33501 0 V2
ath_001.dat 16 50000/mV 16 0 14721 52508 0 V3
ath_001.dat 16 50000/mV 16 0 16103 51083 0 V4
ath_001.dat 16 50000/mV 16 0 6662 44197 0 V5
ath_001.dat 16 50000/mV 16 0 -3806 11333 0 V6
#SL12: sinus bradycardia with marked sinus arrhythmia, Right Axis Deviation, Borderline ECG
#C: Sinus arrhythmia,  Normal ECG


Usage Notes
The intended use of this database is for the development of better algorithms designed to make better diagnostics for athletes based on ECG. One of the unique features of this database is that the ECGs are annotated by both a trained cardiologist and by a state-of-the-art ECG software (GE Marquette SL12).

To get started in Python you can use this code to import the ECG-signals and metadata


import wfdb
import numpy as np
import os

directory = "./your/directory/"
ECGs = []
for ecgfilename in sorted(os.listdir(directory )):
    if ecgfilename.endswith(".dat"):
        ecg = wfdb.rdsamp(directory  + ecgfilename.split(".")[0])
        ECGs.append(ecg)
ECGs = np.asarray(ECGs)


The numpy array (ECGs) now contains all ECG signals and metadata.

Despite the fact that the measurements were taken from top-trained athletes it is not confirmed whether they had athletic remodeling of the heart or not. No echocardiographic or other examinations were performed to investigate the structure of the heart.


References
Fagard R. (2003). Athlete's heart. Heart (British Cardiac Society), 89(12), 1455–1461. https://doi.org/10.1136/heart.89.12.1455
Sanjay Sharma, Ahmed Merghani, Lluis Mont, Exercise and the heart: the good, the bad, and the ugly, European Heart Journal, Volume 36, Issue 23, 14 June 2015, Pages 1445–1453, https://doi.org/10.1093/eurheartj/ehv090
Corrado, D., Basso, C., Pavei, A., Michieli, P., Schiavon, M., & Thiene, G. (2006). Trends in sudden cardiovascular death in young competitive athletes after implementation of a preparticipation screening program. JAMA, 296(13), 1593–1601. https://doi.org/10.1001/jama.296.13.1593
Marijon, E., Tafflet, M., Celermajer, D. S., Dumas, F., Perier, M. C., Mustafic, H., Toussaint, J. F., Desnos, M., Rieu, M., Benameur, N., Le Heuzey, J. Y., Empana, J. P., & Jouven, X. (2011). Sports-related sudden death in the general population. Circulation, 124(6), 672–681. https://doi.org/10.1161/CIRCULATIONAHA.110.008979
