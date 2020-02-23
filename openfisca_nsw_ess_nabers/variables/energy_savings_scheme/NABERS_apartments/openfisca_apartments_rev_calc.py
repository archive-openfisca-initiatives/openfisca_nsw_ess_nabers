# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

from pandas import pandas as pd
import numpy as np
float_formatter = "{:.9f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

# xlsx = r'/Users/liammccann/DPIE/Energy Savings Scheme - 02_Rule as Code/01_ESS/01. 8.8 NABERS/1. Data/climate_zones_postcodes.xlsx'
# df1 = pd.read_excel(xlsx, "postcodes")
# df2 = pd.read_excel(xlsx, "climate_zone")
# df1.index = df1.Postcode
# df2.index = df2.Climate_id
# measured_electricity_consumption input at Step 1
# measured_gas_consumption input at Step 1
# onsite_unaccounted_electricity input at Step 1
# nabers_electricity input at Step 1
# hours_per_week_with_20_percent_occupancy input at Step 3
# net_lettable_area input at Step 3
# building_area_type input at Step 3

# coal_in_KG input in unit_conversions
# coal_KG_to_kWh input in unit_conversions
# diesel_in_L input in unit_conversions
# diesel_in_kWh KG input in unit_conversions
# gas_in_MJ input in unit_conversions
# gas_MJ_to_kWh input in unit_conversions

# add from filename import function to init.py

# postcode = 2042
#
# climate_zone_value = df1.loc[df1['Postcode'] == postcode, 'Climate_zone'].values[0]
# hdd = df2.loc[df2['Climate_id'] == climate_zone_value, 'Hdd'].values[0]
# cdd = df2.loc[df2['Climate_id'] == climate_zone_value, 'Cdd'].values[0]

# %% user inputs


class apartments_benchmark(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Benchmark star rating for the relevant NABERS rated apartment' \
            ' building.' # need to write in condition for method one

    def formula (buildings, period, parameters):
        return buildings('benchmark_nabers_rating', period)


class apartments_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Postcode for the relevant NABERS rated apartment building.' # col C

    def formula(buildings, period, parameters):
        return buildings('postcode', period)


class number_of_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of apartments located in the NABERS rated apartment' \
            ' building.' # col D


class number_of_central_ac_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of centrally air conditioned apartments located in the' \
            ' NABERS rated apartment building.' # col E


class number_of_condenser_water_serviced_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of condenser water serviced apartments located in the' \
            ' NABERS rated apartment building.' # col F


class number_of_lift_serviced_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of lift serviced apartments located in the NABERS rated' \
            ' apartment building.' # col G. note in Claudia's working, this is identical to total number of apartments - this may not always be true :()

    def formula(buildings, period, parameters):
        return buildings('number_of_apartments', period)


class pool_input(Enum):
    no_pool = u'Apartment building does not have a pool.'
    unheated_pool = u'Apartment building has an unheated pool.'
    heated_pool = u'Apartment building has a heated pool.'


class pool_input_status(Variable):
    value_type = Enum
    possible_values = pool_input
    default_value = pool_input.no_pool
    entity = Building
    definition_period = ETERNITY
    label = 'notes whether the complex has no pool, heated pool or unheated' \
            ' pool.' # col H


class pool_status(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'pulls through the pool status.'

    def formula(buildings, period, parameters):
        pool_status = buildings('pool_input_status', period)
        return pool_status


class apartment_has_gym(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'gym boolean value used to indicate whether the complex has no' \
            ' gym or a gym.'  # col I


class input_number_of_naturally_ventilated_parking_spaces(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of naturally ventilated parking spaces located in the' \
            ' NABERS rated apartment building.' # col J


class input_number_of_mechanically_ventilated_parking_spaces(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of mechanically ventilated parking spaces located in the' \
            ' NABERS rated apartment building.' # col K


class number_of_naturally_ventilated_parking_spaces(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of mechanically ventilated parking spaces located in the' \
            ' NABERS rated apartment building.' # col K

    def formula (buildings, period, parameters):
        nat_spaces = buildings('input_number_of_naturally_ventilated_parking_spaces', period)
        number_of_apartments = buildings('number_of_apartments', period)
        mech_spaces = buildings('number_of_mechanically_ventilated_parking_spaces', period)
        condition_nat_parking = nat_spaces < (2 * number_of_apartments - mech_spaces)
        return where(condition_nat_parking, nat_spaces, (number_of_apartments * 2 - mech_spaces))


class number_of_mechanically_ventilated_parking_spaces(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of mechanically ventilated parking spaces located in the' \
            ' NABERS rated apartment building.' # col K

    def formula (buildings, period, parameters):
        mech_spaces = buildings('input_number_of_mechanically_ventilated_parking_spaces', period)
        number_of_apartments = buildings('number_of_apartments', period)
        condition_mech_parking = mech_spaces < (number_of_apartments * 2)
        return where(condition_mech_parking, mech_spaces, (number_of_apartments * 2))


class apartments_elec_usage(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'elec usage in kWh for the relevant NABERS rated apartment complex' \
            ' entered by the user.' # col L

    def formula(buildings, period, parameters):
        return buildings('elec_kWh', period)


class apartments_gas_usage(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'gas usage in MJ for the relevant NABERS rated apartment complex' \
            ' entered by the user.' # col M

    def formula(buildings, period, parameters):
        return buildings('gas_in_MJ', period)


class apartments_gas_kWh_usage(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'gas usage in kWh for the relevant NABERS rated apartment complex' \
            ' entered by the user.' # col M (converted)

    def formula(buildings, period, parameters):
        return buildings('gas_MJ_to_KWh', period)


class apartments_total_kWh_usage(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'total energy use in kWh for the relevant NABERS rated apartment' \
            ' complex entered by the user.' # col L + col M. need to check if this is only elec + diesel

    def formula(buildings, period, paramters):
        elec_kWh = buildings('apartments_elec_usage', period)
        gas_kWh = buildings('apartments_gas_kWh_usage', period)
        return elec_kWh + gas_kWh


class elec_perc_kWh_usage(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'finds percentage of total kWh usage that results from the NABERS' \
            ' buildings entered by the user.' # col N

    def formula(buildings, period, parameters):
        elec_kWh = buildings('apartments_elec_usage', period)
        total_kWh = buildings('apartments_total_kWh_usage', period)
        return np.round((elec_kWh / total_kWh), 2)


class apartments_not_air_con_serviced(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the number of apartments which are not serviced by' \
            ' either Central AC or condenser water.' # col AA

    def formula(buildings, period, parameters):
        AC_apart = buildings('number_of_central_ac_apartments', period)
        cond_water_apart = buildings('number_of_condenser_water_serviced_apartments', period)
        total_apart = buildings('number_of_apartments', period)
        return total_apart - (AC_apart + cond_water_apart)


class pool_parameter_coefficient(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'returns coefficient based on whether complex has pool, as parameter' # col AE and col AF

    def formula(buildings, period, parameters):
        pool_status = buildings('pool_status', period)
        return parameters(period).energy_savings_scheme.NABERS_apartments.pool_coeff[pool_status]


class interceptor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'returns interceptor coefficient' # col AN

    def formula(buildings, period, parameters):
        return parameters(period).energy_savings_scheme.NABERS_apartments.intercept


class central_AC(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Weighting of the central AC coefficient against the number of' \
            ' apartments with Central AC divided by the number of total' \
            ' apartments.' # col AO

    def formula(buildings, period, parameters):
        AC_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.AC_coeff
        number_of_AC_apart = buildings('number_of_central_ac_apartments', period)
        number_of_apart = buildings('number_of_apartments', period)
        central_AC = ((number_of_AC_apart * AC_coeff) / number_of_apart)
        return central_AC


class condenser_water(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Value for condenser water serviced apartments, found by' \
            ' multiplying condenser water coefficient by no. of condenser' \
            ' water serviced apartments, then dividing by total number' \
            ' of apartments.' # col AP. Claudia's sheet has this value to 5dp.

    def formula(buildings, period, parameters):
        CW_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.condenser_water_coeff
        number_of_CW_apart = buildings('number_of_condenser_water_serviced_apartments', period)
        number_of_apart = buildings('number_of_apartments', period)
        condenser_water = (number_of_CW_apart * CW_coeff / number_of_apart)
        return condenser_water


class lifts(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Value used to weight the amount of apartments serviced by lifts' \
            ' in the relevant NABERS rated building.' # col AR

    def formula(buildings, period, parameters):
        lift_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.lift_coeff
        number_of_lift_apart = buildings('number_of_lift_serviced_apartments', period)
        number_of_apart = buildings('number_of_apartments', period)
        lifts = (number_of_lift_apart * lift_coeff / number_of_apart)
        return lifts


class car_park(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Weighting of the number of mechanically ventilated carpark spaces' \
            ' against the mechanically ventilated coefficient, plus the' \
            ' number of naturally ventilated carpark spaces weighted against' \
            ' naturally ventilated carpark coefficient, divided by the total' \
            ' number of apartments.' # AV

    def formula(buildings, period, parameters):
        mvcp_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.mech_ventilated_carpark_coeff
        nvcp_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.natural_ventilated_carpark_coeff
        no_mech_vent_parking_spaces = buildings('number_of_mechanically_ventilated_parking_spaces', period)
        no_nat_vent_parking_spaces = buildings('number_of_naturally_ventilated_parking_spaces', period)
        number_of_apart = buildings('number_of_apartments', period)
        car_park = ((no_mech_vent_parking_spaces * mvcp_coeff) + (no_nat_vent_parking_spaces * nvcp_coeff * mvcp_coeff)) / number_of_apart
        return car_park


class predicted_energy_emissions(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Predicts the total energy emissions of the relevant NABERS' \
            ' apartment building, by adding the Intercept, Central AC,' \
            ' Condenser Water, Lifts, Pools, Gyms and Car Parks values together.'

    def formula(buildings, period, parameters):
        pool = buildings('pool_parameter_coefficient', period)
        has_gym = buildings('apartment_has_gym', period)
        intercept = buildings('interceptor', period)
        central_AC = buildings('central_AC', period)
        condenser_water = buildings('condenser_water', period)
        lifts = buildings('lifts', period)
        gyms = parameters(period).energy_savings_scheme.NABERS_apartments.gym_coeff[has_gym]
        car_park = buildings('car_park', period)
        predicted_emissions = intercept + pool + central_AC + condenser_water + lifts + gyms + car_park
        return predicted_emissions

class emissions_ratio(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "emissions factor weighted by star rating" # col AX via VLOOKUP. need to rewrite as parameter

    def formula(buildings, period, parameters):
        benchmark = buildings('apartments_benchmark', period)
        return select(
            [benchmark == 0
            , benchmark == 1
            , benchmark == 1.5
            , benchmark == 2
            , benchmark == 2.5
            , benchmark == 3
            , benchmark == 3.5
            , benchmark == 4
            , benchmark == 4.5
            , benchmark == 5
            , benchmark == 5.5
            , benchmark == 6]
            ,
            [185.5
            , 159.00
            , 145.75
            , 132.50
            , 119.25
            , 106.00
            , 92.75
            , 79.50
            , 66.25
            , 53.00
            , 39.75
            , 26.5]
            )


class actual_GHG_per_apartment(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'models the actual greenhouse emissions per apartment, by' \
            ' dividing by the relevant emissions ratio for the target' \
            ' star rating.'

    def formula(buildings, period, parameters):
        emissions_ratio = buildings('emissions_ratio', period)
        predicted_emissions = buildings('predicted_energy_emissions', period)
        return predicted_emissions * emissions_ratio / 100


class actual_GHG_KG_CO2 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the actual greenhouse emissions in KG of CO2,' \
            ' produced from the electricity consumption of the building.'

    def formula(buildings, period, parameters):
        actual_GHG = buildings('actual_GHG_per_apartment', period)
        number_of_apartments = buildings('number_of_apartments', period)
        return actual_GHG * number_of_apartments


class actual_GHG_KG_CO2_elec (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the actual greenhouse emissions in KG of CO2,' \
            ' produced from the electricity consumption of the building.'

    def formula(buildings, period, parameters):
        actual_GHG_KG_CO2 = buildings('actual_GHG_KG_CO2', period)
        elec_perc_kWh_usage = buildings('elec_perc_kWh_usage', period)
        return actual_GHG_KG_CO2 * elec_perc_kWh_usage


class actual_GHG_KG_CO2_gas(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the actual greenhouse emissions in KG of CO2,' \
            ' produced from the electricity consumption of the building.'

    def formula(buildings, period, parameters):
        actual_GHG_KG_CO2 = buildings('actual_GHG_KG_CO2', period)
        elec_perc_kWh_usage = buildings('elec_perc_kWh_usage', period)
        return actual_GHG_KG_CO2 * (1 - elec_perc_kWh_usage)


class predicted_electricity_kWh(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The predicted electricity consumption of the relevant NABERS' \
            ' rated apartment building, in kWh. also known as the benchmark' \
            ' rating.' # need to code in condition - if less than zero, = 0. Note that this is identical to the benchmark figure, and to the Maximum Energy Consumption within the offices calculator.

    def formula(buildings, period, parameters):
        actual_GHG_KG_CO2_elec = buildings('actual_GHG_KG_CO2_elec', period)
        apartment_elec_GHG_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.elec_ghg_coeff
        return actual_GHG_KG_CO2_elec / apartment_elec_GHG_coeff


class predicted_gas_MJ(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The predicted gas consumption of the relevant NABERS' \
            ' rated apartment building, in MJ. also known as the benchmark' \
            ' rating.' # need to code in condition - if less than zero, = 0.

    def formula(buildings, period, parameters):
        actual_GHG_KG_CO2_gas = buildings('actual_GHG_KG_CO2_gas', period)
        apartment_gas_GHG_coeff = parameters(period).energy_savings_scheme.NABERS_apartments.gas_ghg_coeff
        return (actual_GHG_KG_CO2_gas / (apartment_gas_GHG_coeff / 3.6))