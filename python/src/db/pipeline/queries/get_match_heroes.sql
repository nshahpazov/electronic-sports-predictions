SELECT match_id,

-- hero_{j} = I(hero_j belongs to radiant team)
sum(hero_id =   1 and player_slot < 128) as "hero_1",
sum(hero_id =   2 and player_slot < 128) as "hero_2",
sum(hero_id =   3 and player_slot < 128) as "hero_3",
sum(hero_id =   4 and player_slot < 128) as "hero_4",
sum(hero_id =   5 and player_slot < 128) as "hero_5",
sum(hero_id =   6 and player_slot < 128) as "hero_6",
sum(hero_id =   7 and player_slot < 128) as "hero_7",
sum(hero_id =   8 and player_slot < 128) as "hero_8",
sum(hero_id =   9 and player_slot < 128) as "hero_9",
sum(hero_id =  10 and player_slot < 128) as "hero_10",
sum(hero_id =  11 and player_slot < 128) as "hero_11",
sum(hero_id =  12 and player_slot < 128) as "hero_12",
sum(hero_id =  13 and player_slot < 128) as "hero_13",
sum(hero_id =  14 and player_slot < 128) as "hero_14",
sum(hero_id =  15 and player_slot < 128) as "hero_15",
sum(hero_id =  16 and player_slot < 128) as "hero_16",
sum(hero_id =  17 and player_slot < 128) as "hero_17",
sum(hero_id =  18 and player_slot < 128) as "hero_18",
sum(hero_id =  19 and player_slot < 128) as "hero_19",
sum(hero_id =  20 and player_slot < 128) as "hero_20",
sum(hero_id =  21 and player_slot < 128) as "hero_21",
sum(hero_id =  22 and player_slot < 128) as "hero_22",
sum(hero_id =  23 and player_slot < 128) as "hero_23",
sum(hero_id =  24 and player_slot < 128) as "hero_24",
sum(hero_id =  25 and player_slot < 128) as "hero_25",
sum(hero_id =  26 and player_slot < 128) as "hero_26",
sum(hero_id =  27 and player_slot < 128) as "hero_27",
sum(hero_id =  28 and player_slot < 128) as "hero_28",
sum(hero_id =  29 and player_slot < 128) as "hero_29",
sum(hero_id =  30 and player_slot < 128) as "hero_30",
sum(hero_id =  31 and player_slot < 128) as "hero_31",
sum(hero_id =  32 and player_slot < 128) as "hero_32",
sum(hero_id =  33 and player_slot < 128) as "hero_33",
sum(hero_id =  34 and player_slot < 128) as "hero_34",
sum(hero_id =  35 and player_slot < 128) as "hero_35",
sum(hero_id =  36 and player_slot < 128) as "hero_36",
sum(hero_id =  37 and player_slot < 128) as "hero_37",
sum(hero_id =  38 and player_slot < 128) as "hero_38",
sum(hero_id =  39 and player_slot < 128) as "hero_39",
sum(hero_id =  40 and player_slot < 128) as "hero_40",
sum(hero_id =  41 and player_slot < 128) as "hero_41",
sum(hero_id =  42 and player_slot < 128) as "hero_42",
sum(hero_id =  43 and player_slot < 128) as "hero_43",
sum(hero_id =  44 and player_slot < 128) as "hero_44",
sum(hero_id =  45 and player_slot < 128) as "hero_45",
sum(hero_id =  46 and player_slot < 128) as "hero_46",
sum(hero_id =  47 and player_slot < 128) as "hero_47",
sum(hero_id =  48 and player_slot < 128) as "hero_48",
sum(hero_id =  49 and player_slot < 128) as "hero_49",
sum(hero_id =  50 and player_slot < 128) as "hero_50",
sum(hero_id =  51 and player_slot < 128) as "hero_51",
sum(hero_id =  52 and player_slot < 128) as "hero_52",
sum(hero_id =  53 and player_slot < 128) as "hero_53",
sum(hero_id =  54 and player_slot < 128) as "hero_54",
sum(hero_id =  55 and player_slot < 128) as "hero_55",
sum(hero_id =  56 and player_slot < 128) as "hero_56",
sum(hero_id =  57 and player_slot < 128) as "hero_57",
sum(hero_id =  58 and player_slot < 128) as "hero_58",
sum(hero_id =  59 and player_slot < 128) as "hero_59",
sum(hero_id =  60 and player_slot < 128) as "hero_60",
sum(hero_id =  61 and player_slot < 128) as "hero_61",
sum(hero_id =  62 and player_slot < 128) as "hero_62",
sum(hero_id =  63 and player_slot < 128) as "hero_63",
sum(hero_id =  64 and player_slot < 128) as "hero_64",
sum(hero_id =  65 and player_slot < 128) as "hero_65",
sum(hero_id =  66 and player_slot < 128) as "hero_66",
sum(hero_id =  67 and player_slot < 128) as "hero_67",
sum(hero_id =  68 and player_slot < 128) as "hero_68",
sum(hero_id =  69 and player_slot < 128) as "hero_69",
sum(hero_id =  70 and player_slot < 128) as "hero_70",
sum(hero_id =  71 and player_slot < 128) as "hero_71",
sum(hero_id =  72 and player_slot < 128) as "hero_72",
sum(hero_id =  73 and player_slot < 128) as "hero_73",
sum(hero_id =  74 and player_slot < 128) as "hero_74",
sum(hero_id =  75 and player_slot < 128) as "hero_75",
sum(hero_id =  76 and player_slot < 128) as "hero_76",
sum(hero_id =  77 and player_slot < 128) as "hero_77",
sum(hero_id =  78 and player_slot < 128) as "hero_78",
sum(hero_id =  79 and player_slot < 128) as "hero_79",
sum(hero_id =  80 and player_slot < 128) as "hero_80",
sum(hero_id =  81 and player_slot < 128) as "hero_81",
sum(hero_id =  82 and player_slot < 128) as "hero_82",
sum(hero_id =  83 and player_slot < 128) as "hero_83",
sum(hero_id =  84 and player_slot < 128) as "hero_84",
sum(hero_id =  85 and player_slot < 128) as "hero_85",
sum(hero_id =  86 and player_slot < 128) as "hero_86",
sum(hero_id =  87 and player_slot < 128) as "hero_87",
sum(hero_id =  88 and player_slot < 128) as "hero_88",
sum(hero_id =  89 and player_slot < 128) as "hero_89",
sum(hero_id =  90 and player_slot < 128) as "hero_90",
sum(hero_id =  91 and player_slot < 128) as "hero_91",
sum(hero_id =  92 and player_slot < 128) as "hero_92",
sum(hero_id =  93 and player_slot < 128) as "hero_93",
sum(hero_id =  94 and player_slot < 128) as "hero_94",
sum(hero_id =  95 and player_slot < 128) as "hero_95",
sum(hero_id =  96 and player_slot < 128) as "hero_96",
sum(hero_id =  97 and player_slot < 128) as "hero_97",
sum(hero_id =  98 and player_slot < 128) as "hero_98",
sum(hero_id =  99 and player_slot < 128) as "hero_99",
sum(hero_id = 100 and player_slot < 128) as "hero_100",
sum(hero_id = 101 and player_slot < 128) as "hero_101",
sum(hero_id = 102 and player_slot < 128) as "hero_102",
sum(hero_id = 103 and player_slot < 128) as "hero_103",
sum(hero_id = 104 and player_slot < 128) as "hero_104",
sum(hero_id = 105 and player_slot < 128) as "hero_105",
sum(hero_id = 106 and player_slot < 128) as "hero_106",
sum(hero_id = 107 and player_slot < 128) as "hero_107",
sum(hero_id = 108 and player_slot < 128) as "hero_108",
sum(hero_id = 109 and player_slot < 128) as "hero_109",
sum(hero_id = 110 and player_slot < 128) as "hero_110",
sum(hero_id = 111 and player_slot < 128) as "hero_111",
sum(hero_id = 112 and player_slot < 128) as "hero_112",

-- hero_{j+112} = I(hero_j belongs to dire team)
sum(hero_id =   1 and player_slot >= 128) as  "hero_113",
sum(hero_id =   2 and player_slot >= 128) as  "hero_114",
sum(hero_id =   3 and player_slot >= 128) as  "hero_115",
sum(hero_id =   4 and player_slot >= 128) as  "hero_116",
sum(hero_id =   5 and player_slot >= 128) as  "hero_117",
sum(hero_id =   6 and player_slot >= 128) as  "hero_118",
sum(hero_id =   7 and player_slot >= 128) as  "hero_119",
sum(hero_id =   8 and player_slot >= 128) as  "hero_120",
sum(hero_id =   9 and player_slot >= 128) as  "hero_121",
sum(hero_id =  10 and player_slot >= 128) as  "hero_122",
sum(hero_id =  11 and player_slot >= 128) as  "hero_123",
sum(hero_id =  12 and player_slot >= 128) as  "hero_124",
sum(hero_id =  13 and player_slot >= 128) as  "hero_125",
sum(hero_id =  14 and player_slot >= 128) as  "hero_126",
sum(hero_id =  15 and player_slot >= 128) as  "hero_127",
sum(hero_id =  16 and player_slot >= 128) as  "hero_128",
sum(hero_id =  17 and player_slot >= 128) as  "hero_129",
sum(hero_id =  18 and player_slot >= 128) as  "hero_130",
sum(hero_id =  19 and player_slot >= 128) as  "hero_131",
sum(hero_id =  20 and player_slot >= 128) as  "hero_132",
sum(hero_id =  21 and player_slot >= 128) as  "hero_133",
sum(hero_id =  22 and player_slot >= 128) as  "hero_134",
sum(hero_id =  23 and player_slot >= 128) as  "hero_135",
sum(hero_id =  24 and player_slot >= 128) as  "hero_136",
sum(hero_id =  25 and player_slot >= 128) as  "hero_137",
sum(hero_id =  26 and player_slot >= 128) as  "hero_138",
sum(hero_id =  27 and player_slot >= 128) as  "hero_139",
sum(hero_id =  28 and player_slot >= 128) as  "hero_140",
sum(hero_id =  29 and player_slot >= 128) as  "hero_141",
sum(hero_id =  30 and player_slot >= 128) as  "hero_142",
sum(hero_id =  31 and player_slot >= 128) as  "hero_143",
sum(hero_id =  32 and player_slot >= 128) as  "hero_144",
sum(hero_id =  33 and player_slot >= 128) as  "hero_145",
sum(hero_id =  34 and player_slot >= 128) as  "hero_146",
sum(hero_id =  35 and player_slot >= 128) as  "hero_147",
sum(hero_id =  36 and player_slot >= 128) as  "hero_148",
sum(hero_id =  37 and player_slot >= 128) as  "hero_149",
sum(hero_id =  38 and player_slot >= 128) as  "hero_150",
sum(hero_id =  39 and player_slot >= 128) as  "hero_151",
sum(hero_id =  40 and player_slot >= 128) as  "hero_152",
sum(hero_id =  41 and player_slot >= 128) as  "hero_153",
sum(hero_id =  42 and player_slot >= 128) as  "hero_154",
sum(hero_id =  43 and player_slot >= 128) as  "hero_155",
sum(hero_id =  44 and player_slot >= 128) as  "hero_156",
sum(hero_id =  45 and player_slot >= 128) as  "hero_157",
sum(hero_id =  46 and player_slot >= 128) as  "hero_158",
sum(hero_id =  47 and player_slot >= 128) as  "hero_159",
sum(hero_id =  48 and player_slot >= 128) as  "hero_160",
sum(hero_id =  49 and player_slot >= 128) as  "hero_161",
sum(hero_id =  50 and player_slot >= 128) as  "hero_162",
sum(hero_id =  51 and player_slot >= 128) as  "hero_163",
sum(hero_id =  52 and player_slot >= 128) as  "hero_164",
sum(hero_id =  53 and player_slot >= 128) as  "hero_165",
sum(hero_id =  54 and player_slot >= 128) as  "hero_166",
sum(hero_id =  55 and player_slot >= 128) as  "hero_167",
sum(hero_id =  56 and player_slot >= 128) as  "hero_168",
sum(hero_id =  57 and player_slot >= 128) as  "hero_169",
sum(hero_id =  58 and player_slot >= 128) as  "hero_170",
sum(hero_id =  59 and player_slot >= 128) as  "hero_171",
sum(hero_id =  60 and player_slot >= 128) as  "hero_172",
sum(hero_id =  61 and player_slot >= 128) as  "hero_173",
sum(hero_id =  62 and player_slot >= 128) as  "hero_174",
sum(hero_id =  63 and player_slot >= 128) as  "hero_175",
sum(hero_id =  64 and player_slot >= 128) as  "hero_176",
sum(hero_id =  65 and player_slot >= 128) as  "hero_177",
sum(hero_id =  66 and player_slot >= 128) as  "hero_178",
sum(hero_id =  67 and player_slot >= 128) as  "hero_179",
sum(hero_id =  68 and player_slot >= 128) as  "hero_180",
sum(hero_id =  69 and player_slot >= 128) as  "hero_181",
sum(hero_id =  70 and player_slot >= 128) as  "hero_182",
sum(hero_id =  71 and player_slot >= 128) as  "hero_183",
sum(hero_id =  72 and player_slot >= 128) as  "hero_184",
sum(hero_id =  73 and player_slot >= 128) as  "hero_185",
sum(hero_id =  74 and player_slot >= 128) as  "hero_186",
sum(hero_id =  75 and player_slot >= 128) as  "hero_187",
sum(hero_id =  76 and player_slot >= 128) as  "hero_188",
sum(hero_id =  77 and player_slot >= 128) as  "hero_189",
sum(hero_id =  78 and player_slot >= 128) as  "hero_190",
sum(hero_id =  79 and player_slot >= 128) as  "hero_191",
sum(hero_id =  80 and player_slot >= 128) as  "hero_192",
sum(hero_id =  81 and player_slot >= 128) as  "hero_193",
sum(hero_id =  82 and player_slot >= 128) as  "hero_194",
sum(hero_id =  83 and player_slot >= 128) as  "hero_195",
sum(hero_id =  84 and player_slot >= 128) as  "hero_196",
sum(hero_id =  85 and player_slot >= 128) as  "hero_197",
sum(hero_id =  86 and player_slot >= 128) as  "hero_198",
sum(hero_id =  87 and player_slot >= 128) as  "hero_199",
sum(hero_id =  88 and player_slot >= 128) as  "hero_200",
sum(hero_id =  89 and player_slot >= 128) as  "hero_201",
sum(hero_id =  90 and player_slot >= 128) as  "hero_202",
sum(hero_id =  91 and player_slot >= 128) as  "hero_203",
sum(hero_id =  92 and player_slot >= 128) as  "hero_204",
sum(hero_id =  93 and player_slot >= 128) as  "hero_205",
sum(hero_id =  94 and player_slot >= 128) as  "hero_206",
sum(hero_id =  95 and player_slot >= 128) as  "hero_207",
sum(hero_id =  96 and player_slot >= 128) as  "hero_208",
sum(hero_id =  97 and player_slot >= 128) as  "hero_209",
sum(hero_id =  98 and player_slot >= 128) as  "hero_210",
sum(hero_id =  99 and player_slot >= 128) as  "hero_211",
sum(hero_id = 100 and player_slot >= 128) as "hero_212",
sum(hero_id = 101 and player_slot >= 128) as "hero_213",
sum(hero_id = 102 and player_slot >= 128) as "hero_214",
sum(hero_id = 103 and player_slot >= 128) as "hero_215",
sum(hero_id = 104 and player_slot >= 128) as "hero_216",
sum(hero_id = 105 and player_slot >= 128) as "hero_217",
sum(hero_id = 106 and player_slot >= 128) as "hero_218",
sum(hero_id = 107 and player_slot >= 128) as "hero_219",
sum(hero_id = 108 and player_slot >= 128) as "hero_220",
sum(hero_id = 109 and player_slot >= 128) as "hero_221",
sum(hero_id = 110 and player_slot >= 128) as "hero_222",
sum(hero_id = 111 and player_slot >= 128) as "hero_223",
sum(hero_id = 112 and player_slot >= 128) as "hero_224"
FROM match_player mp
GROUP BY match_id;
