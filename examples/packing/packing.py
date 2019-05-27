#%PDF-1.3 40 0 obj << /Length 370 /Type /EmbeddedFile >> stream
import pypdfplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel('data.xlsx')
plt.plot(df.x,df.y,'r-')

with open('title.txt','r') as f:
    title = f.readline()
    xlabel = f.readline()
    ylabel = f.readline()

plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.pack(['data.xlsx',
          'title.txt'])

plt.publish()
#plt.cleanup()

"""
endstream
endobj
1 0 obj
<<
/Producer (PyPDF2)
>>
endobj
2 0 obj
<<
/Type /Catalog
/Pages 3 0 R
/Names <<
/EmbeddedFiles <<
/Names [ (data\056xlsx) <<
/F (data\056xlsx)
/Type /Filespec
/EF <<
/F 38 0 R
>>
>> (title\056txt) <<
/F (title\056txt)
/Type /Filespec
/EF <<
/F 39 0 R
>>
>> (packing\056py) <<
/F (packing\056py)
/Type /Filespec
/EF <<
/F 40 0 R
>>
>> ]
>>
>>
/PageMode /UseAttachments
>>
endobj
3 0 obj
<<
/Kids [ 4 0 R ]
/Count 1
/Type /Pages
>>
endobj
4 0 obj
<<
/Parent 3 0 R
/Contents 5 0 R
/Type /Page
/Resources 6 0 R
/Group <<
/CS /DeviceRGB
/S /Transparency
/Type /Group
>>
/MediaBox [ 0 0 576 432 ]
>>
endobj
5 0 obj
<<
/Length 1940
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789ca5564d6f1c370cbdeb57e8d81c4c4b14a5918e31da04e8cdeda23d1b4ed2d8c83ab01dc3e9bf
efd3e7cc6667760314c67a4451e2e393f821abef95d5ff68a3eff17bd556bf5706a3bdf653c0f74b
f98a638c4cfb7e569fd4e55bec7ac6d47b3531e689f3161b49aaf0a5092e468a90b0a80ff3f647dd
778984bc4c3c05fdf451ffad1ff4e55bceb659ff0e77eef1cb6e65a7fe28609613d6ee750c14a3b6
d6918d02bbd65882af09b02964d9060aa2a327ef8aec2c79d693903358af6c410e529cb2c1124790
25c3c5d814c806ed0da5a96c4e96b00b5b82cf321b4f297b4f268882cc06761a757660139b32cb30
835df3e6e0496436ced1906335c03979d8699e396bc8c4e1b6762c047e83967389c0bfd356ce0be5
531ae7e2423eaf7a6a90a290e0d864a2498a3a2582211b260a36af102bc4a26c4cc475025b2d6bb6
4cbe6c11fc6737157be263be0686b7aec0c9e4f23570628ac521c1bde3181cc3a1e2b1372e5f84f3
9e6ca174102aea4f75ad1f0f83e0b5075a5db33fdab188bc63e57a801e28e6f0c47483368036488d
1c83b83ffd7ab81e0798ad5c2ddd2ac3726d986f66e0bd7a5439802f0c8480abf6c94d5e3bdc2b3e
b77b75b5d397ef2cae48ef3ea97cdd5e4284cae8dd07f58b356ff4ee5efdb68319e8b02ae7c23c82
81cbbf3e3edd5cecef1e5e9ef5af5fd535fe3a89e2780df5e67b13bafb55ec0cba749a8475912653
9dfc591afe7fb358e4d8be275c6751c5cea24b2b2c0e9c648b2c9890943c786457cb816bb87a085f
b2b2c35761c01771c037e92c3c72c405313fc0fb55f89ac60dbe091dbe8a1dbe4be7e05d7038fe23
78bb4e3f277d432fc38e9d858e5cc7e77005a5c3bb7484bbce7b25b507f632d3e7bc3f87ef2d1a41
f2ce1ee2f3e07d78495324d3621d3555eae2effae6fbddf3fa8672fb1735ea57292dea48e8d5e8ea
47a23257aa6d2ae85a9d08ba403c19bf408d39b90b6a19cda84d5151876ef300b12a57b088f8e998
7e13b4f7eb6934a101db551577d66e46ce849e96ef8103baf588d76de8896b5d0e6db8806eaa063d
b467a1915c32a0b759e7d659804b0f1db075ba8276cd266420e0e4b61be288d16d409f7a48d5e102
b4a91aecd09e01467f1e21c5db4c9de11e5575b8c8cca6aac0b3f614702a6419af92115b6e9b757d
3856f0325c803755031fdaf3e04e780e2f7782796ffb61bc1e8e6b922cde2227c15b3bc5c36ec497
98f59a947bf045eec6e8c3d5658bf75f6c556ab72f4ff86ce0dfd532955dca858af393afd67f3108
eb867afd72f3e1e9e6dbddad7ef7f270fbedeeebc39681dae79203b965b1bb56ff018cd58ca5>
endstream
endobj
6 0 obj
<<
/Pattern 7 0 R
/ExtGState 8 0 R
/Shading 9 0 R
/XObject 10 0 R
/Font 12 0 R
/ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]
>>
endobj
7 0 obj
<<
>>
endobj
8 0 obj
<<
/A2 <<
/CA 1
/ca 1
/Type /ExtGState
>>
/A1 <<
/CA 0
/ca 1
/Type /ExtGState
>>
>>
endobj
9 0 obj
<<
>>
endobj
10 0 obj
<<
/Vera-minus 11 0 R
>>
endobj
11 0 obj
<<
/Length 75
/Filter [ /ASCIIHexDecode /FlateDecode ]
/BBox [ -184 -236 1288 929 ]
/Type /XObject
/Subtype /Form
>>
stream
789ce33234305330363555c8e532373602b372c02c237323200b248b604164d300015f0a0a>
endstream
endobj
12 0 obj
<<
/F1 13 0 R
>>
endobj
13 0 obj
<<
/FontMatrix [ 0.001 0 0 0.001 0 0 ]
/FirstChar 0
/Widths 14 0 R
/FontBBox [ -184 -236 1288 929 ]
/Encoding <<
/Type /Encoding
/Differences [ 32 /space 48 /zero /one /two /three /four /five 70 /F 81 /Q 97 /a 99 /c /d 105 /i 110 /n /o 114 /r /s /t /u 120 /x /y ]
>>
/Type /Font
/BaseFont /BitstreamVeraSans-Roman
/CharProcs 15 0 R
/LastChar 255
/Subtype /Type3
/FontDescriptor 37 0 R
/Name /BitstreamVeraSans-Roman
>>
endobj
14 0 obj
[ 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 600 318 401 460 838 636 950 780 275 390 390 500 838 318 361 318 337 636 636 636 636 636 636 636 636 636 636 337 337 838 838 838 531 1000 684 686 698 770 632 575 775 752 295 295 656 557 863 748 787 603 787 695 635 611 732 684 989 685 611 685 390 337 390 838 500 500 613 635 550 635 615 352 635 634 278 278 579 278 974 634 612 635 635 411 521 392 634 592 818 592 592 525 636 337 636 838 600 636 600 318 636 518 1000 500 500 500 1342 635 400 1070 600 685 600 600 318 318 518 518 590 500 1000 500 1000 521 400 1023 600 525 611 636 401 636 636 636 636 337 500 500 1000 471 612 838 361 1000 500 500 838 401 401 500 636 636 318 500 401 471 612 969 969 969 531 684 684 684 684 684 684 974 698 632 632 632 632 295 295 295 295 775 748 787 787 787 787 787 838 787 732 732 732 732 611 605 630 613 613 613 613 613 613 982 550 615 615 615 615 278 278 278 278 612 634 612 612 612 612 612 838 612 634 634 634 634 592 635 592 ]
endobj
15 0 obj
<<
/F 16 0 R
/four 17 0 R
/space 18 0 R
/Q 19 0 R
/three 20 0 R
/o 21 0 R
/n 22 0 R
/i 23 0 R
/s 24 0 R
/d 25 0 R
/c 26 0 R
/a 27 0 R
/r 28 0 R
/y 29 0 R
/x 30 0 R
/one 31 0 R
/u 32 0 R
/t 33 0 R
/zero 34 0 R
/five 35 0 R
/two 36 0 R
>>
endobj
16 0 obj
<<
/Length 150
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c333537553050b0b40012a686e60ae646960a29865c403e8895cb0513cb01b3cc4ccc802c434b
649689b1219065626186c43236b180ca225806401a6c4d0eccf41cae340003711893>
endstream
endobj
17 0 obj
<<
/Length 183
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c4d8d4112c0200803efbc224f5044d0ff747ad2ff5fabd40ebdc04e0289164582f4356a4b30ee
b832156b5029989497c055305c0bdaeea2cafe32494c9d86d37bb70383b2f17183d249fbf6717a00
abfd7a06dd0fd21c2258>
endstream
endobj
18 0 obj
<<
/Length 35
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3336b4503080c314432e001a9402ec>
endstream
endobj
19 0 obj
<<
/Length 509
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c35513b72053108eb7d0a2eb0330663b0cff332a992fbb79120db2c5a3e42c27952a6ec9047ed
482e9574932f1debba4498fc8e6556c8624bac2d664bf631f90c3d2a1b631a531c1c8c2b9c15204b
1376e8bd35a31ea890e59a34a9f416a49de40136637583a4db63461184651132f60a222e65074570
a6659184429bd3e4b582ca82a4054ffc2dc73f63fb7aa163e85125322fe45a97419c1521747aa105
510fb848ce0867570bd9845fd8f623e7227fe060276f6c4e99fffa013cafa0bab3bb63b19de339e1
f6f65b70012356df28b433ab83fd3d9373160bdf8fa48cbd85c8985187305cebccf7b2f87239481d
cfd897f98cef3f6bd462ee>
endstream
endobj
20 0 obj
<<
/Length 685
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c355239aedd400ceb7d0a5d208076cd9ce705a97eeedf86945f0a43b4568a9a8e169569f96521
552d932ebfed496d891bf2f7c90a8913925725daa50c9150f93c8554bf67cbbcbed69c11204b950a
939392c7250bfe0c97de2e1ce7636b3f8f23773d7a60558c841201cb1413a36b593abbc39a8dfc3c
a6013fe21172ae58b71c6315480dba71da15ef43f379c81a206698968a0a5d5689167e41f1a047ad
7df758545820d1ed1c49708c8d5091807681da480c39b316bba82ffa5994980974ed8b22eea2c012
49cc9c625d3afa0f3e742ca8bf36e3cbaf8e4afa482b6b4cda77a34969cc2293ae97456f376f7d3d
b840f32eca7f5ecd204153d628697cd0aa9d63289a196585771c9a0c34c71c87cc133c87331294f4
7d287e5f4b26ba28913f0e0da17f5f1ea38c9c066f0173d19fb68a0317f1d961af1c6085d2c59ae4
7d402a137a60faffd7f879fefc031cb68054>
endstream
endobj
21 0 obj
<<
/Length 434
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3d50bb11433108eb3d050be4ce7ced37cfcba5cbfe6d249ca442364212949a4cc994873aca92
ac294f1d3e4b6287bc87e56e6436252a452f93b025f7d00af17d89e614f7ddd596b343349768397e
0b332aaa1b1dd34b369a702a13baa0dcc333fa0d6d740356871eb15b20d0a460d7b62072c70f180c
c199138b220c4a4d06ffad72f752dcef3d1c6fa2889474f0aef9e5f4cbcf2dbc4e3d8e44babdf98a
6b71a63a0a4470466af28a7461c5b2c843a4d504353d036bb500aede7af9376847741980ec1389e3
34a51c43ffd6b8c7eb03878a52f4>
endstream
endobj
22 0 obj
<<
/Length 327
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c45904b12c3200c43f79c4247f047067c9e74ba4aefbfad214db380a7b14006772704a9b50513
d1052f6d4bba0b3e5b09cec678e8366e3512e404758056a4e36894527db9c5699574f16836732b0b
ad131d660e7a94a319a0103a15deeda2e472a6eecef94770f55ff547b1ee9ccdc4c064e50e8466f5
29ee7c9b1d515ddd647fd2636ed66b7f15f6aab0b4aca5e584dbce5d33a004eea91cedfd05a9733a
84>
endstream
endobj
23 0 obj
<<
/Length 138
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3332b7503050b03401128616260ae666060a29865c40bea989b9422e17480cc4ca01b30c80b4
259c82885b42344194825810a56626661049380322970600c9b415e5>
endstream
endobj
24 0 obj
<<
/Length 673
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c2d52398e24310ccbfd0a7e6000ebf2f19e1e4cd4fbff7449550505aa6ccb3ce472c344257e2c
90db516be2d74666a0c2f0afabcc85ef48dbc83a886bc8455cc996c267442ce431c43cc482efdbf8
191ef9acccc9b307c62fd9f71956eca909cb42c68b33b4c32a8ec32ac8b160eb22aa7b7853a4c3a9
24d8e38bff3ec573178216be2368c02ff9e7ab2378bea445da3d66dbb45b0f96694795149683ed69
cecbe44beb2c57c7e3f920d9de153b426a5780a23077c6792e8e326d65446b616783a4c6c5f6e6d8
8fa5045de8c665a43802f9992ac2034a9acc6ca220fec8e921a73210a6aee94a27b7511577eac95c
b3b9bc9d49325bf7458acd14ceebc299f5779832abcd3b799613a54e45f8197bb6040d9de3ead96b
998546b739c12b257c36767a72f2bd9a590fc9a9484815d3ba0a4ea3c8144bd896f89a8a9ad2d4cb
f0df97f7197fff0133e27c01>
endstream
endobj
25 0 obj
<<
/Length 460
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c354f3bb203210ceb39852e90198c6d60cfb399542ff76f9f64b20d12fe48f2f44447265ee6c8
08acd9f1b616198819f81653f1af3dedc384ea3db88708e5e2429861249c35ebb89ba7e3c5bf5de5
33d6c1bb0dbe62961704b63093f595c599cb76c1581a27714eb21b63d7446c635debe914d6114c28
03219ded3025c81c15297db2a38c393a4ee489e762aac52ebfef617dc1a631a2c21c57054fd06450
963def26a01d17f4dfd58ddf49348b5e02329160619d24e6ce594ef8d56b47c7518b223127a419e4
3211d29cae620aa109c53a3b0a2a150597ea73cadd3eff685d5b4d>
endstream
endobj
26 0 obj
<<
/Length 466
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3551496ec3300cbceb15f38100e22ebfc7414fedffaf1dd2096060684b9ccd111b1b117889c1
cf41e4c65bd68c9af89bc95df1bb3c151e09b7822751045e867bd9092e6f1897fd38cc7cf05e5a39
931a4f322017d9f4f044c8609740e8c0ec1ad4619b6927fa8684cf8e48351b594e5f4bd04bab1028
4fd97ea70b4ab4adeacfedb32eb4ed6b4f38d9eda927954f209e5bb202978d574c166319f444e52e
c5f441aab3859e84f2a27c0eb2f9a821125da29c81270607a3403bb0e7b69f895785a075759fb68d
a11a291d4fff3634354922e413259cd9d2b85bf8fe9e7bfdfc03a654539f>
endstream
endobj
27 0 obj
<<
/Length 616
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3d923b92c3300c437b9d8217c88cf893e4f3642795f7feed3e32c95680498900282f7599b2a6
3c20692609ffd1e1e1623be577d89ecdccc0b5442f13cb29cfa12bc4dc45f9b2998dbab23ac5aac3
309d5bf4a89c8b864d939ae72a4b19b70b9ec3b589e7967dc40f3734a807758d4bc20dddd568590a
cd7075ff3bbd47d977353c179b54ead4178f175115e6f9214fa287e94ae27c3c28215c7b30461612
e453d1408eb35cadf25e42f60eb71ab2c2416a49e7b3273cd8757a4f2e6e17cd100f64b954f84e51
ecedd033beec4a093d12b6e158ee7d3b9ab1e91a9b38ec7eef46d6ca8cae68217ec85727eb2560dc
53264512644eb6586e8bd59eeea128a67386731920ead98a8652e66257ab7f0c3b6f2c2fd92cc894
cc0b3246a74d9e3878c87e8d9af47995e778fd016cf3733b>
endstream
endobj
28 0 obj
<<
/Length 318
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c4590b911433108447355410912b008eab1c7d177ffa917f94ab46f002d87af2553aa1f2722a6
dcd768f430790e9f4d25562cd826b6931a721b16414a3198784e31aba3b7a19987d4ebb8a8aab875
6695d369cbcac57ff3685733933dc235ea27f04de8f89f3cb4a9e85ba0af0b947d40b5389d495031
7daf6281a39c767f229c18e03e194799292371626e0aecf7190066be57b8c6e305dd013779>
endstream
endobj
29 0 obj
<<
/Length 280
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3d8f410e03310803ef79853f1029764258deb3554fdbff5f4b9add5ed0088c311642436fa86a
0e9b820dc78ba54ba8d6f0298a894a0ec899600ea5a4d21d67917a623818dc1eb41bcee2b1e9fa11
bb92567dd0e646ba25688247ec5369dc967113c4033505ea29ea5ca3bc10b99fa957d83492ddb4b2
926b38a6dfbde7a9ebffd355de5f5fdf2e8c>
endstream
endobj
30 0 obj
<<
/Length 177
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c354db911c03008eb998211cca3d8ec934be5ecdf06ecb8413a7d20941b6be40182e19d6f21f8
a62f198475084f2abb253a6ca186b30a9289e157367855ae8af6b59289ec6ca631d8a065fad1ceb7
49cf07a5de1b98>
endstream
endobj
31 0 obj
<<
/Length 163
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c458cbb0dc03008447ba660047e26669f2895b37f1b204adc704fba7bb83a123253de61868704
9e0c2c8653f10699a36035b846528d9deca3b06e5f7581e67a53abf5f7072a4f7676713dcdcb19f4
>
endstream
endobj
32 0 obj
<<
/Length 331
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c4d903b0ec3300c43779f82170820eae3cf7952746aefbf567212a083c107ca902875730866e0
a021bcdec08b2d1d65c7b7a0ac4fe3f827e5ba897d80f98bbaa0922a86b3a906c68046a03b74f592
b3997b814dc3587012a4a4efb640273c2c9bd956b55195b07bec93ee2249addaa3d30b8c0881670c
edb00cb0bb9b4f1c01e3b5a6a65f9a29e99bd8331f98b7f0489b4264885acaf771ea14677bff003f
eb3833>
endstream
endobj
33 0 obj
<<
/Length 266
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c458fcb0d04210c43ef54e112f2193ea987d59ed8feafeb309a4142f841223bf13008acf3f236
d0c5f0d1a2c337fe36d5ab63952c1fba7a52560fe99087bcf21550693051c485594c1d4361ce98ca
c89632b71be1b64d83ac6c9554ad83763c060fb6a765ab087ea96d61ea2cf10cc2555eb8c70d3f90
4bad77bd55be7f42533097>
endstream
endobj
34 0 obj
<<
/Length 426
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c3550cb0d433108bb670a16a8140281649e56bd75ff6b6dd03b6111ff4258c8940879a9c9ce29
e94b3e3a4c0fb62ebfb1220bad7525ecca9a209e2befa199b2b1d1d8e260701a265e80163760e869
8d1a3574e182a62e954281c525f0997c757be8be4f19786a197276041143c960096aba164d58b43c
9f904e01e2ff7ec3ee2de4a192f3ca9e1bf91b9cedf03bb36ee1276a7622d1721532d4b334c71808
13451e3c7945a670e2b3d677d53412d4660b4e9601ae4e3f8c0e0060225e5980ecae44394bd28ea5
9f6fbcc7f70f400053b4>
endstream
endobj
35 0 obj
<<
/Length 501
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c4d51bb6d44310cebdf145ce000eb6b799e0b525df66f43c90890c220a12f29a72516f6c64b0c
e1075b0fbee49155437f1e3f31ec332c3dc9e4d43fe6b9c95414be15aa9b98501762e1fd6804bc16
742f222bca07df8f650c73cef7e0a3109760263460ac6f492617d5bc3364c289a18ec3419b541877
4d142cae15cd33c8ed5637b23ab3206c782513e2c6004404d91790cd60a38cb19590c5721ea80a92
055a60d7e91b518b822b94d60974a2d6c4bacce0abe7f67637432ff2e0a8ba787d0ceb4bb0c2e8a5
7b2c7cae421fccf44c3b774923bdf0a61311660f0552999d91953a3d627db740ff9f652bf8fbc9cf
f3fd0b15285c2a>
endstream
endobj
36 0 obj
<<
/Length 503
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c2d513992034108cbe7157a4273d3efb1cb91f7ffe90aca01838643203a2d7150c64f10962bde
f2c855b4e1ef9918c177c1a1dfca751b1639101548d218544da85dbc1ebd07761c6602f3a4352c83
19eb033f630a377a71784cc6d9ed751935047bd76b4f6650322b1771c9c4055375d8c899c34fa68c
0bed5ccf0dc8b911d66518a49b95c68c84234d215248a1ea26a933419004a3ab51a38d1cc57ee9cb
239d6155236a0cfb5c4bdbd77313ce1a343b16ab3c39a547579ccbc9c50b2b07fdbccdc045541aab
3c101270bfdb43fd9cece437ded2b9b3c5f4f85e73b2bc301558f1e6b51b904db5f8372fe2f83de3
ebf9fc03a8a55b16>
endstream
endobj
37 0 obj
<<
/FontBBox [ -184 -236 1288 929 ]
/StemV 0
/Descent -236
/XHeight 547
/Flags 32
/Type /FontDescriptor
/FontName /BitstreamVeraSans-Roman
/Ascent 929
/ItalicAngle 0
/MaxWidth 1342
/CapHeight 730
>>
endobj
38 0 obj
<<
/Length 12776
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789ced59655854ebda1eba1be91a24454a1aa4bb91920607868681a1a591ee6e09411a941610a453
babb534ae9fe70ef73aeede6787e9f1fdfbee79a35ef3b6b9e67cd5aef73bf4fa9c8c3c1e3031001
c800000008c8786a0db1820100b01100003c0032acae38c4d6116ceb68a8ee660776d06771b5b1a6
7a070fcb90058005fc83ffd728896f516a63430f3c90f92c9ec06459692f825c3afbaa19878e9d82
8a669f8459f11d2fe9ececaaa9b1584189d8b7f72f48afeebe7c72a6abd437ae60861f1b48b4d60b
d742d4e47fbf576472d0b7799d01260ad068e545a39d85ab983ebeb4ac98736f0eaf604e2c891c16
b68bac0894325a7eae3553a8672e913bf971c5a0bb5a0be60b79c4fe27476ebf08376bae29c71fc8
0953c9c9827b5b47be343ea289fd58bea52f7bfccfa4e47142e221a597ebb194e4a8bd0aec5a5651
3cfe2daef9e20d47b52dec07097278557ed640310f1c8c57876f9733594a84d375093725f919f435
2c507a7b14c51f310c2161a35af94c2553974a3eaebad9105acdf48bc9073f6793716fa2996bc3d9
f686531eecc3895588027636c290d5efca560dd611c08ce9a27312bf81bb1edb5f8e6eed7653647e
6687a354bf795d08216c71cb45c13cf4f639c0b1a9745016c37e17381aedcc75d5139377b78227ee
fe8541857ce1f9bcd928ebfd63bebb8303a8fc8da3d51a6c8f8fef470af71444bbe7a821146cedc0
caf2f3f80f37ffc14f94c42a2affc9cdeba0eeb3f1f9686c317917519906a0ba978fec1c5675440e
0de9fc177a326c75923770d2de8d5ed7bdb3f3cf2376ba81a72b9c2561b8f8028f6b5c4a03932eed
9d909ed04113a5ec4b96db719cc74fc64f53a4e5dc189c1ba39e147f2ac896ef597c2c35fa5da21c
7b90e525090ade7bb24002c1145f9d4e45ed05d07919ccb898da5e69e0c75a9eac9db8c134efc9c4
bc6d0ce1603e85dd919447dd0e20b3e9328f6e6be0c90589869a399fc5475006949fdacdd0c4baf9
4822ed0bde8d07b3527ab72a3527eef9b341e92edaac136f9d2aceef7d6fddda7950da8abb0f7bfc
c2280b16607e479258a4f85df8fb33c2700000090019c6d59af54f9eb840a0562008c4eaa72bfb37
6760ee3903f3bf5eb3ff354a62fb2cdbd9d025cf026edf0c37d93ff35409b4371d564db649f3f2b1
8be7550021e97aae1d58a9f2f73447db56b0cbb49e518434cc7abb949ed35092983d329145f52b71
061b5b211c74f4f53f0e6e3697b77e4b8b008730b539f9b2e1a565cc6abe51aa507001e80d6cdb1c
e43dfa8c4a10d05e709ab730fd20da78db6a3a4708a4088dcbc31a19e4a2121ec50f52f5158eafa5
0acd8e1ab8b36a28b2e41414b8198e594723787638d48920e1db44a779a84b1f83b306beea4f3d25
1b148bbbd2eafdde9f4854c145dc942e8c28de8ed755f8688d57dbbfce104fcab838139ddbd98faf
3a91055a6bc980fefac9e254d7d7c14a76c85d4b77e5d4a630e07736d437e83f19756f175feff753
acfb6fee6de857eb098f5584ac5261071e309d0853eda37442df3184aa315a166f54ec64cf66a084
1be337c17f52babd89b471ab5465156cf9dacc71d0f7d1fdb38e781315dd9ebee24545167cfab15c
8383e2dde72f4fb9e3739fa6e3760a146c63e07ace095fcf9c0819282d1822c3ea1559a4394c3d4b
3441d3cc7d8fb5f471e4dc5cb2932d431b15c75f8e59a4263041b2dc54d35c9abe95fbd67f394d4a
def54745e5d20ff8102309a98bc271603f2793b75f25b541fdc7e8054489f4aae10b6e31c672a8fb
7301ca8e9eac3d26c37e93392f715de61ce5a61e798972d9359e2f9f8dd29513cf1aa448cf9333de
06637ba10938b2c713c5fca81c2156579c24baa4d80f098d9d0a10cfc7d074d34840005f79e7b886
c19713afe88e198a2d1c22d3a2920ca75c471aa790829a4a7aa18273e452e7d9d9ca2e5fb163bfe5
3bf79e7131335de3d6f2ad2034890b270a55f7ee65811c061bfd846aebf2d2fca27aa7bccfed0fa7
4cf542483128c3550aec15c891e4b720c5f67851c9d26ed64db401315b10adce37c5d08e7cbc23e9
b93b84dfad9deb7e3f5ae6fda8f5fe8dffe7da3998bf82824dd41ca116b6660e3f1750225214b595
0d5bf2cccf05b9b2b6503f582696055e390b0979cf1cae3fd7346f64612138b8ef4c08abc92289b7
88d01433e4e96e3109be6ad2a508165aed37b00b7cc74ae1993175d5476af16f35a46d4f8baada09
1063b673b95ce0a4063552a37ba1ca7caf19932953f3c39b36615eac14a4d50b6d6dc1f9ee8c2880
b261b8d45c075c6fcb39c8d2716a899807b6b03c3a2e09eb3dec20bf35c6371f76562310018055d2
9f91f91f37e4680eb601ff7964ff793fbbdafdb6a43cd84d845b02d8eeca4fa7638d8963e0e41357
b8ed415372a164858faafb921bf4a2e3c9e743d7b4b24486abb6de8b4004f16de0684458b7473f29
0ee78918648b436963081ecd86f8de76205a875cd9f3a6674671cc154f5298a093e3021907d35e9c
4069c568a22e7c366439ea47bf19e88445abf3521a753a8c84774a484d722f781f3c3178c9d883ec
7751a7d7d5cfa051a465a813cb8e6eec964248136426cef2ac64a95826111196d2772e9c99f9e593
6279e23c377f68baefd46c1b300265c72266b853c235a865524f56109ba3fc83241e24b00513b388
04d855d10fcfdf5e42dcc20fe735f6184bdd9f281195823327f4222491bb8c65f9048aab86b6c17f
54bf919ffe528988ec691a97e448268bcede04c9cb9abc1f183e856e7af9a3162e456a6e883eab44
ce964ef6e0897aabf109893cb80aca4d702dd3895c7f97c08f971b8eb6553aa5af73c63a50b9a8ae
cab9830c8b4b26b893043fc3687b78621a5ad9d4cc16532cf83cf572c25c6c1cd12abd70859323ee
c7da189ac99eb765f4442586d690fb7f80f128556d3563080eb470dca60d7cfe320cc4dc7656b705
2b0247acc9296da9170d8c0486cef27e430b7dacbe942e4f54f0f4657dc2a3f3626fab0d3545d6a8
4914e78de96cad010c0bc5e8700466758e4bec5c29ccb5f1a3034341ef5003416fe8f5e1f4f7b6cc
484a417eaff39c8475c5b94eb715258f8b3d336faf1bf6cbd56d1e564a6f9c4e79c2bb6f5899d73f
8e365f51ad4d5adfb13679fc98ada4676dba3c3e3ba0405a4a833dd3778d329578a7bb86bcf71dfd
d4147dd54ae972c583e33563de027abadfaecf56a49ce05229bb29502fecbcb381c94747acf95bce
5546d95521112389d68554aa5b33f980765858168ced563519da99941bae815eb8de1c45675076f5
2cef99de2cf1a3e642ec8aa31a487ebb9a43d2b2deb2ff9a04f0269c121b37d9394a75b04c809340
ef47b6d81983e52b124ed9a8d3469154c5993ce27330992ab6dedeb4e9268ba53dc1cc0901df714c
34763242fc01ce46ca777e0ac6f4008953bb4ebd378bed4f3018eb8409cac3bec920642821af1670
50a9066ecc117c34ecdae661fba83db427609d7e2193bd252ab3a1f8b52e6c6e05690fdf4c52c52c
359fe514ce0d000c1d6679093cc73ce390f046125ef2c86e38505da9bb72a4fe248ea7fc5edb678b
fe31cee1ba53eb8d075925902e10ec73284831687ecbaf6a86af75035f38b918532f98a0147b4947
e6933d362324ba1e66772706bbd89ae3912432f0356e4be0d6ab6b71d83be30be1fa8f8ecad3f002
df3633a7fac299ca00c9abe867351f3ac3e7e2f36c93ec9e63d4b39993a08e6a28a57da20e880287
2d2de3faf693d17cba0c2e7214ee40883fd718f5a3abc07f2ba36e8792f08598bb9f8d0f385b558b
8fea3e5a38e184659c220eaa6e437276edd8d3c807296ca6267bb9560c8512d84d7468967d9e0769
148f8b555ee816938ca333bed64db325f6e0fdc24594ae83b743013f8eabe5f6a80cbd6a7f08e395
14e2cc7e4d54e6274956cf6c9658468ae811e9d78b47424524f48a2030ae140ce576d3113e255f31
57d554add6de5325685231b396ed4a63edf791dce90c37d9cdbd104793bab4f4a7d2d2fd052f0ccb
a4193a253948c4d230282b613fb338158668c3ba6894e372ef2a2b9ae2957140b85b5f6907a4e159
9dd561b83f57412eacf9a860639e2c0d46fe38a7874a7493f4cd68226cc627e298670804c6f05b86
8cc2ee6e3524a207d1689655bec57160020168137ec4508384c9c9b285484304d1f727b351af8855
50ce808138c7849f664627b8a33ca02c71038d2a1cbc0291da312bb1b64ea14acfa65b1529949dd8
164b6aa404a774555c2aeb8e201db9d708361d18ab77d39ac76eb084f84c707bbe44b6890852fc86
6938844fd69bc524e556cb7cacb8dac8b199ed04d1a380054b5eb3d7846b2a77b57c66e0e4aa4021
b5bd617814d4cd1839046083883cdda5128e26f3200b536c829f8204df4e6f6bd13c7d90ff092752
d94ea5a018a37ffdabb85844f47d93eb8bc53ef41dfafaee8b7c4d21ee94415d8aad9de6442de75b
62ab9854f1cb811743c8199e7979a9232d5698a70e14d589e51bce9ff5848f5ee83673e1cdb13005
872487264f27d15e8aec7d175cd2843f10b2760ba02a629d6e85b3f0ab3a9e0a6aedc19c311a7967
dda2aa594b6820d582e1a6bdad3419f0d4334eee2cbd3383c0ec166ac0d2d474f93cb35c1ecdbdc6
9969dea71068a19c57c0124517116e1feed6b7d184bc7a73b5b4c5ecbace06929b4942c15a52c5a9
47bf1a818d5de49f54983f47fb9df70a1b327c16781f4695df3b6b8c7fb96347376bf01f7e3857dd
0692c6867d2b6471d7f2c3c5320b8886a3c2ac18f3c46934d779a489df08b7d84bb4663b56f1ea40
104eb680df66f41261917c7333c3ddc1b93a095690ddb84e932f92452c3cb9c8b17f9cbbcb90b2d7
c837c6497d5cddbc03ea614460f8e860113c410edfb0c8be812dc290b6fad6612f165b772f39f754
ac56a125538a5496bcc054deda8aa8b4f40b0d42489b9d12cd3a2a16b2bcf60d5a70ee46b9d51bb9
be44fea665bf06f1a8809892c45addf718f3c859f551a655fca0b35e26d71ea69c52db3984669c79
cecfa00fda7934b43eea26119a03efe45c7a454b0133d25a424f6ef4136e9378300d244dbdb3e89f
34e3be5235492098a1424a8001354abee8418cb27a72de697730a1d2d3f18aad6b6188d0e1388e4c
f5486ac52d3c28405e2f18af780a0f201e23ea44c651048f10f1a32d3be0109584aff9d8cbfbfb02
c9ebe01513a8ef314c98758e22c61b87b2ae6175133f2ecc6092a6f98bd16d8226d23d32f5ba6e4b
a55a9d17cb6ac4224ab0b96aecc0fd1b3b4f2b03a303d25c7e6d3917dd4da2ce31c2650631ea1cde
258cd0aecc7718539040c9ab0d5a212a25f32f549ea8511e5f1caea7216f7c7a88814379abadf627
a4ad3eda0783b4c89e48e999bb4dbcf90c2a21a95c5578fbcbc71c5d661778c56ef4ab719384b7b9
fa5831ab95cf5ddf0b21ce3608a0ad22d0efa00f7e1f4c1b0f72f454eb6ca1d663f69ba695f7e3d4
2e7d63e2dca8f3a18f33bced9b619ca47b5beac9a0684c0b88b9d407cc695c611c7a66a61b49dffb
96b2caab14792803aabcea76ce1ed29af5193dc7883b3fcc88fd8b82dfb39095138f9a7ad95e9356
c10be1fd1732efcc5dfb9e5f986c7f32f12b36fe10499eaa932d9b750b44c9945b44817a598599fd
36dc4ae0e1d3a7820700e8710100a2bf627f077330d8d181f58f8f3f62aef864fda819fe3f930089
3a43bfb7cdb07eea431ae39a45ead5829b3f64e878b16d70f34392f66eaf22bb3c4836189ae4e9da
3e53b85fbb7ebd6ecb2c423fadd843d56015e3260af42de1a866dcd9a3bede9ccc0f922572d41923
7d51a4c3d2ca331d40397276b0f1a1c873df597507403d364f3d6731fff55d419f7305eebc085745
206b9d2553f672f5bc94fea85c790ba506b83da8cd5e3de41da68dbff62c7d60ef11759cf213f742
93529b68cd44b1b6f306fd61c72e738d097a3dda99cda40da09a061c7042527b8b079d045183fbaa
a25483698276ed2688965aa0b33329ed5023a6ba48ad8e42e45337e631f7a6056704952aff227eb4
6fca6956c205b55ec5f4938d57f103f67eb7cc6b562edfc9cccb6f19e5532cea7c9d50e138eeacde
6744ac12b261004d8230e972bb1dcb9328c1da2cad1f9e07725d473cd920a67917d7b97ef4e200af
6cfa8c7baa5bef73fc65d0eb9ba7617b4a6f0e91379a153aac8f4e691ad02700b9481e8e24e77143
d46f6b77b87c4efced9d23d8c65b4cd32fc1fc83e107b8e9402d24b7ddd1e5e7336d43156db5e3eb
3cce9704be5f65d156ce26570a7e34eb911b0f8ed2de450de6cca1fb630cb2bc849a2ab9e713e8d6
15c625b06f261f2b5541f166e4b43a2a1f714ce37f2aea3be74c468979bdc291d81e095e09ef48fe
d0095acfd63adde6ad135e5741bfd9343271a224d737ce738c3bf2d7efbf999276b176ea8a2c6357
abff3e7d2177362c7d36bc1349f6f30717f7f349b64f2ea58a25fb6e3d762ea5e1292360892635ca
f9c2f188b71e112923b489492dc0355f0cf126cf4b80c0290971a792e6c48d9fa9573348f3e233d3
9eba78fc5d8a95d8349aa14f5043bc84873eec3a080f8fccd8800a0e92fb4e6052a6c2b167a0845a
a5e3b316c282d4bea905c42820683694b6f2917034de84514f2c1e3f8a5fcad1d79cb1a76d73b841
542e1369298fed3355b9f63bd84c811bfb169c8bf1e7a2c933635fc3404b3615768c81a67229ad44
472b44aeabd3ab8933fad1e4d0bce6fecf32880b52d38285430aeb0ae41a7361e0259bf8f94ae2fe
f8674ebc0eac89be674ed53af1d929aa793338737e8d834c873511899543e6f46169967d1f27f73e
7836a7c8db05436b3956875245e3224b89d1dd7b585dbb0a9bc6c25ce770a3eabac5affaad973c61
52c7fc9b498fd78514cb3b481d2e105fec1fee1508d221773522232d6821b0ac0c296d08d29210ee
77f01e4ad91042cdf3abf824f9f625f9ee67b58292028582ef7e9cae90d5a61bb36c0d29592a079f
4436ca202d24d786f157a9cdb0d3ef3c3f0591bbe69cf63bedda2e3a171cb92aec42d644efd2b2de
93bbb06660072c18f760eced222c2c549396272c4a3430efb030802309a10577130b534170ae1345
ec93c7d2cd2d3a16a545abb398b7d1317617149859185f1346ba088fe85bb659338e7f5fbafdb81b
6f200c0300bcb87785380064181388b10a1462e7c06a0c8182ffd55cf9a718750f8f5843f93636fc
8e45842fe23dee69eddbc9d97b2260654c78a65008b06e36b49f32d6bc160299b1ad7e035ca33d4b
bf6aa04f5aeb6bb48ca5b46be2ae17e17ccc00c31c5e72522302197fa29fd58e54460b090f84256f
ce01bb7926a0f5f9db1fae8423105a1ecad2580cfa330fb1c0f7b19d829042af9ef23be2f3743252
ac8cdb94afaf84416016b19f75a1c2263db79b835113c01dc661ec08ae5a2cdb8651353217f1c5a4
180d5f118600f2af3b020d527835c831b99bb6895c7a1341d8d2670b9339e536b3256f4fd8415ea1
c213831f6ed446755c1a707d7af550e9c80e8df45256b76959ca96854a562379b8ba83c4c758c772
b75631b1a365d19b033fd1af7b9e9eab97aa4cefb1d19e31be7de9fff1d6c3f9f1e0658388b82839
d29d7c6e18a71863e156f8fc02bb1c7d3b9e51b7e72d4aaf21e0775637d422c470783feabdb73a6c
c01fbeccf895b5b1b8f92b0bdb9f4667123b2fd7ce862d7580b008fcda9846a73f4999cac2700eff
0dce9fdb16ed825116dbd33d67aa6ca381f1d891688078865c381d7c4097c7e72a099ac4e6f0425e
dd1d0c355066e5396b579df01ae376cdd91aa5e13f9d7c399fb577f87c7bbab2a2855e526da0eff1
a64572f8a80521c16a5f522df6db8175ae0c379d77c3c6a9e13d03d0694ea4fd5ed89d065f4949e5
0a5a6e4214d0e9550f4fd3dd3a21146d0db08629637131ed3d7da4125743b674a7a0ebf184da8a7a
22a557af792df513a30869ae28b1bf28a1094a776be078ae2d000823051b0fcf8b121dcb80509bb8
75b1e9ef718576f57b4ed6233fa30bfdd9f284fbf9747ee1e42b3bbb7f28f917d2634521b36ce801
0770a794e8f3a47cfa3ce8be25207981e3a15730b1ce668a79c6d91534c12531c7935135c363d3ce
33116beeae9712b2fa94fc86c7d1c31d2a21ebeff011e049ad084f135ca73c1bce9fa2d2e059ae1a
fbc891c174547bdd29d94015a27b6008c8703ee232bfd0910da9091858f25b6f96c373300b9efd9c
546e911e90669e29804cc3daf723ce1f4eb420bb49265f849db6ecf5e5e210ff8c2f16a54b577bb3
8ea76c8f805530a4f08b40dae3cec0d0d937081fd6f4d4156a11aed2c9c99d0ad73e6be85a3d2fe1
d3e2e97ccc70c1ade26214f8de26bcaf4043b998e269875e96fb72b57ee84a922891dd93e1b45d05
aa4e126b358e092120f8866383de1a0639c1a48d93acafcec5a081a9910c432f9d34c807c53fc0a1
fded63acf39ce964853b2a838110e9c01097d68b1d454172be2e52c857a41b9cc648fd67cbddad85
f52ecb2894232c0b447e93361958e3355cc4965e3ea335ca704e5d615fbd90b56be976b3bd4eae99
d12177bc9e768dd79f1884e3af4b2a53622186da7788ffb65f185866c07f6bda3fc46f5af80f15fc
bda3f82b72ef49f14b7ff1a1e0dfbb2cbfa207f18f7de6bff45c1eea795869ff0b1828ff51777f28
fcb0d4fbcb9f40fd7de1f7a18687b5d5bf908af6db4aeb43050fd3dbbfa085fb20d97d28fa30d1f8
0b288ffe7bdaf150cbdf038b5f61480c00fc4798f150fca187f80be3a4ffe92f1e4aff7d07fd1547
64bf5cfc5ffba98a3c02e2cf7368f7afa6fbeb5552fe9cfd1f02d23651>
endstream
endobj
39 0 obj
<<
/Length 77
/Filter [ /ASCIIHexDecode /FlateDecode ]
>>
stream
789c0b2c4d4c294a2cc94c56702bcd4b2ec9cccfe3e5aa5048acc82ce6e5aa04d300d5e00bce>
endstream
endobj
xref
0 41
0000000000 65535 f 
0000000451 00000 n 
0000000491 00000 n 
0000000838 00000 n 
0000000897 00000 n 
0000001061 00000 n 
0000003094 00000 n 
0000003239 00000 n 
0000003260 00000 n 
0000003359 00000 n 
0000003380 00000 n 
0000003421 00000 n 
0000003647 00000 n 
0000003680 00000 n 
0000004115 00000 n 
0000005168 00000 n 
0000005421 00000 n 
0000005664 00000 n 
0000005940 00000 n 
0000006067 00000 n 
0000006669 00000 n 
0000007447 00000 n 
0000007974 00000 n 
0000008394 00000 n 
0000008625 00000 n 
0000009391 00000 n 
0000009944 00000 n 
0000010503 00000 n 
0000011212 00000 n 
0000011623 00000 n 
0000011996 00000 n 
0000012266 00000 n 
0000012522 00000 n 
0000012946 00000 n 
0000013305 00000 n 
0000013824 00000 n 
0000014418 00000 n 
0000015014 00000 n 
0000015229 00000 n 
0000028100 00000 n 
0000000009 00000 n 
trailer
<<
/Size 41
/Root 2 0 R
/Info 1 0 R
>>
startxref
28269
%%EOF
0000029184
"""
