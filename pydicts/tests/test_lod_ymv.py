from decimal import Decimal
from pydicts import lod_ymv

def tests_lod_year_month_value_transposition():
    o=[
        {"year": 2022, "month": 1, "my_sum": 12},
        {"year": 2021, "month": 2, "my_sum": 123},
        {"year": 2019, "month": 5, "my_sum": 1},
        {"year": 2022, "month": 12, "my_sum": 12},
    ]
    t=lod_ymv.lod_ymv_transposition(o,key_value="my_sum")
    assert t[0]["year"]==2019
    assert t[3]["total"]==24

def tests_lod_ymv_transposition_with_percentages():
    o=[
        {'year': 2007, 'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': Decimal('673.420708'), 'total': Decimal('673.420708')}, 
        {'year': 2008, 'm1': Decimal('675.290000'), 'm2': Decimal('676.693600'), 'm3': Decimal('678.143600'), 'm4': Decimal('680.077800'), 'm5': Decimal('682.077700'), 'm6': Decimal('684.066600'), 'm7': Decimal('686.693400'), 'm8': Decimal('688.976400'), 'm9': Decimal('691.204200'), 'm10': Decimal('693.323500'), 'm11': Decimal('695.197600'), 'm12': Decimal('696.811800'), 'total': Decimal('8228.556200')}, 
        {'year': 2009, 'm1': Decimal('698.369800'), 'm2': Decimal('699.044640'), 'm3': Decimal('699.605900'), 'm4': Decimal('699.651500'), 'm5': Decimal('700.358200'), 'm6': Decimal('701.290400'), 'm7': Decimal('702.576900'), 'm8': Decimal('703.238700'), 'm9': Decimal('704.174500'), 'm10': Decimal('704.765900'), 'm11': Decimal('704.954900'), 'm12': Decimal('705.687800'), 'total': Decimal('8423.719140')}, 
        {'year': 2010, 'm1': Decimal('705.792600'), 'm2': Decimal('706.240800'), 'm3': Decimal('706.816500'), 'm4': Decimal('706.845800'), 'm5': Decimal('706.185000'), 'm6': Decimal('705.700900'), 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': Decimal('710.218060'), 'total': Decimal('4947.799660')}, 
        {'year': 2011, 'm1': Decimal('711.104600'), 'm2': Decimal('711.649500'), 'm3': Decimal('712.384100'), 'm4': Decimal('713.220700'), 'm5': Decimal('714.362200'), 'm6': Decimal('715.415800'), 'm7': Decimal('716.354600'), 'm8': Decimal('718.111300'), 'm9': Decimal('719.274200'), 'm10': Decimal('720.421000'), 'm11': Decimal('720.365000'), 'm12': Decimal('725.471500'), 'total': Decimal('8598.134500')}, 
        {'year': 2012, 'm1': Decimal('728.814700'), 'm2': Decimal('729.283100'), 'm3': 0, 'm4': 0, 'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0, 'total': Decimal('1458.097800')}, 
        {'year': 2013, 'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0, 'm9': Decimal('758.550000'), 'm10': 0, 'm11': 0, 'm12': 0, 'total': Decimal('758.550000')}, 
        {'year': 2014, 'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': Decimal('768.387330'), 'total': Decimal('768.387330')}, 
        {'year': 2015, 'm1': Decimal('768.600000'), 'm2': Decimal('768.790000'), 'm3': Decimal('768.860000'), 'm4': Decimal('768.890000'), 'm5': Decimal('768.810000'), 'm6': Decimal('769.050000'), 'm7': Decimal('769.060000'), 'm8': Decimal('769.010000'), 'm9': Decimal('768.950000'), 'm10': Decimal('768.910000'), 'm11': Decimal('769.070000'), 'm12': Decimal('768.970000'), 'total': Decimal('9226.970000')}, 
        {'year': 2016, 'm1': Decimal('768.940000'), 'm2': Decimal('768.830000'), 'm3': Decimal('768.810000'), 'm4': Decimal('768.750000'), 'm5': Decimal('768.690000'), 'm6': Decimal('768.520000'), 'm7': Decimal('768.340000'), 'm8': Decimal('768.460000'), 'm9': Decimal('768.270000'), 'm10': Decimal('768.150000'), 'm11': Decimal('768.000000'), 'm12': Decimal('767.850000'), 'total': Decimal('9221.610000')}, 
        {'year': 2017, 'm1': Decimal('767.670000'), 'm2': Decimal('767.490000'), 'm3': Decimal('767.260000'), 'm4': Decimal('767.090000'), 'm5': Decimal('766.870000'), 'm6': Decimal('766.650000'), 'm7': Decimal('766.410000'), 'm8': Decimal('766.070000'), 'm9': Decimal('765.790000'), 'm10': Decimal('765.490000'), 'm11': Decimal('765.150000'), 'm12': Decimal('764.800000'), 'total': Decimal('9196.740000')}, 
        {'year': 2018, 'm1': Decimal('764.440000'), 'm2': Decimal('764.080000'), 'm3': Decimal('763.640000'), 'm4': Decimal('763.290000'), 'm5': Decimal('762.450000'), 'm6': Decimal('762.130000'), 'm7': Decimal('761.880000'), 'm8': Decimal('761.430000'), 'm9': Decimal('761.090000'), 'm10': Decimal('760.680000'), 'm11': Decimal('760.060000'), 'm12': Decimal('759.750000'), 'total': Decimal('9144.920000')},
        {'year': 2019, 'm1': Decimal('759.610000'), 'm2': Decimal('759.390000'), 'm3': Decimal('759.160000'), 'm4': Decimal('758.870000'), 'm5': Decimal('758.390000'), 'm6': Decimal('758.280000'), 'm7': Decimal('758.110000'), 'm8': Decimal('757.710000'), 'm9': Decimal('757.360000'), 'm10': Decimal('756.950000'), 'm11': Decimal('756.570000'), 'm12': Decimal('756.180000'), 'total': Decimal('9096.580000')}, 
        {'year': 2020, 'm1': Decimal('755.990000'), 'm2': Decimal('755.450000'), 'm3': Decimal('751.600000'), 'm4': Decimal('752.320000'), 'm5': Decimal('752.750000'), 'm6': Decimal('753.350000'), 'm7': Decimal('753.410000'), 'm8': Decimal('753.390000'), 'm9': Decimal('753.110000'), 'm10': Decimal('752.940000'), 'm11': Decimal('752.420000'), 'm12': Decimal('752.030000'), 'total': Decimal('9038.760000')}, 
        {'year': 2021, 'm1': Decimal('751.640000'), 'm2': 0, 'm3': 0, 'm4': 0, 'm5': Decimal('750.040000'), 'm6': 0, 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0, 'total': Decimal('1501.680000')}, 
        {'year': 2022, 'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0, 'total': 0}, 
        {'year': 2023, 'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'm6': Decimal('748.982000'), 'm7': 0, 'm8': 0, 'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0, 'total': Decimal('748.982000')}
    ]
    from pydicts import lod
    r=lod_ymv.lod_ymv_transposition_with_percentages(o)
    lod.lod_print(o)
    lod.lod_print(r)
    assert 1==1# Change to 2 to debug
