"""Mock data for Phoenix and San Diego regions with real lat/lng."""

from solver.models import (
    Depot,
    EquipmentType,
    Location,
    Property,
    PropertyType,
    Region,
    Vehicle,
    VehicleStatus,
)

# ── Phoenix Region ──

PHX_DEPOT = Depot(
    id="depot-phx-1",
    name="Verde PHX Yard",
    location=Location(lat=33.4373, lng=-111.9838),
    region=Region.phoenix,
)

PHX_PROPERTIES = [
    Property(id="phx-p01", name="Scottsdale Quarter HOA", address="15059 N Scottsdale Rd, Scottsdale, AZ",
             location=Location(lat=33.6175, lng=-111.9263), property_type=PropertyType.hoa, lot_acres=12.0, region=Region.phoenix),
    Property(id="phx-p02", name="Gainey Ranch Estates", address="7700 E Gainey Ranch Rd, Scottsdale, AZ",
             location=Location(lat=33.5654, lng=-111.9162), property_type=PropertyType.residential_estate, lot_acres=8.5, region=Region.phoenix),
    Property(id="phx-p03", name="Kierland Commons", address="15205 N Kierland Blvd, Scottsdale, AZ",
             location=Location(lat=33.6219, lng=-111.9292), property_type=PropertyType.retail, lot_acres=5.0, region=Region.phoenix),
    Property(id="phx-p04", name="Honor Health Scottsdale", address="7400 E Osborn Rd, Scottsdale, AZ",
             location=Location(lat=33.4797, lng=-111.9183), property_type=PropertyType.medical, lot_acres=6.0, region=Region.phoenix),
    Property(id="phx-p05", name="Tempe Marketplace", address="2000 E Rio Salado Pkwy, Tempe, AZ",
             location=Location(lat=33.4317, lng=-111.9009), property_type=PropertyType.retail, lot_acres=15.0, region=Region.phoenix),
    Property(id="phx-p06", name="ASU Research Park", address="7700 S River Pkwy, Tempe, AZ",
             location=Location(lat=33.3873, lng=-111.8998), property_type=PropertyType.commercial, lot_acres=10.0, region=Region.phoenix),
    Property(id="phx-p07", name="Chandler Fashion Center", address="3111 W Chandler Blvd, Chandler, AZ",
             location=Location(lat=33.3062, lng=-111.8713), property_type=PropertyType.retail, lot_acres=20.0, region=Region.phoenix),
    Property(id="phx-p08", name="Dignity Health Chandler", address="1955 W Frye Rd, Chandler, AZ",
             location=Location(lat=33.2907, lng=-111.8674), property_type=PropertyType.medical, lot_acres=7.0, region=Region.phoenix),
    Property(id="phx-p09", name="Mesa Riverview", address="1061 N Dobson Rd, Mesa, AZ",
             location=Location(lat=33.4380, lng=-111.8726), property_type=PropertyType.commercial, lot_acres=8.0, region=Region.phoenix),
    Property(id="phx-p10", name="Gilbert Town Square", address="1100 S Gilbert Rd, Gilbert, AZ",
             location=Location(lat=33.3316, lng=-111.7899), property_type=PropertyType.municipal, lot_acres=4.0, region=Region.phoenix),
    Property(id="phx-p11", name="SanTan Village", address="2218 E Williams Field Rd, Gilbert, AZ",
             location=Location(lat=33.2982, lng=-111.7555), property_type=PropertyType.retail, lot_acres=18.0, region=Region.phoenix),
    Property(id="phx-p12", name="Mountain Park Ranch HOA", address="3400 E Baseline Rd, Phoenix, AZ",
             location=Location(lat=33.3774, lng=-111.9859), property_type=PropertyType.hoa, lot_acres=25.0, region=Region.phoenix),
    Property(id="phx-p13", name="Paradise Valley Town Hall", address="6401 E Lincoln Dr, Paradise Valley, AZ",
             location=Location(lat=33.5310, lng=-111.9439), property_type=PropertyType.municipal, lot_acres=3.0, region=Region.phoenix),
    Property(id="phx-p14", name="Camelback Corridor Offices", address="2555 E Camelback Rd, Phoenix, AZ",
             location=Location(lat=33.5092, lng=-111.9677), property_type=PropertyType.commercial, lot_acres=4.5, region=Region.phoenix),
    Property(id="phx-p15", name="Desert Ridge Marketplace", address="21001 N Tatum Blvd, Phoenix, AZ",
             location=Location(lat=33.6780, lng=-111.9760), property_type=PropertyType.retail, lot_acres=22.0, region=Region.phoenix),
    Property(id="phx-p16", name="Mayo Clinic Scottsdale", address="5777 E Mayo Blvd, Phoenix, AZ",
             location=Location(lat=33.6595, lng=-111.9570), property_type=PropertyType.medical, lot_acres=12.0, region=Region.phoenix),
    Property(id="phx-p17", name="Ahwatukee Foothills HOA", address="4700 E Warner Rd, Phoenix, AZ",
             location=Location(lat=33.3350, lng=-111.9850), property_type=PropertyType.hoa, lot_acres=30.0, region=Region.phoenix),
    Property(id="phx-p18", name="Tempe Town Lake Business Park", address="430 N Scottsdale Rd, Tempe, AZ",
             location=Location(lat=33.4310, lng=-111.9274), property_type=PropertyType.commercial, lot_acres=6.0, region=Region.phoenix),
    Property(id="phx-p19", name="Scottsdale Airpark Business Center", address="15444 N 76th St, Scottsdale, AZ",
             location=Location(lat=33.6247, lng=-111.8993), property_type=PropertyType.industrial, lot_acres=10.0, region=Region.phoenix),
    Property(id="phx-p20", name="McCormick Ranch HOA", address="7600 E McCormick Pkwy, Scottsdale, AZ",
             location=Location(lat=33.5500, lng=-111.9190), property_type=PropertyType.hoa, lot_acres=15.0, region=Region.phoenix),
    Property(id="phx-p21", name="Chandler Municipal Complex", address="175 S Arizona Ave, Chandler, AZ",
             location=Location(lat=33.3032, lng=-111.8414), property_type=PropertyType.municipal, lot_acres=5.0, region=Region.phoenix),
    Property(id="phx-p22", name="Superstition Springs Center", address="6555 E Southern Ave, Mesa, AZ",
             location=Location(lat=33.3932, lng=-111.7216), property_type=PropertyType.retail, lot_acres=14.0, region=Region.phoenix),
    Property(id="phx-p23", name="Gilbert Heritage District", address="50 E Vaughn Ave, Gilbert, AZ",
             location=Location(lat=33.3526, lng=-111.7888), property_type=PropertyType.municipal, lot_acres=3.5, region=Region.phoenix),
    Property(id="phx-p24", name="Val Vista Lakes HOA", address="2929 S Val Vista Dr, Gilbert, AZ",
             location=Location(lat=33.3190, lng=-111.7545), property_type=PropertyType.hoa, lot_acres=20.0, region=Region.phoenix),
    Property(id="phx-p25", name="Phoenix Industrial Park", address="4020 S 36th St, Phoenix, AZ",
             location=Location(lat=33.4103, lng=-111.9783), property_type=PropertyType.industrial, lot_acres=8.0, region=Region.phoenix),
]

PHX_VEHICLES = [
    Vehicle(id="phx-v01", name="PHX Truck 1", crew_size=3, equipment=[EquipmentType.standard, EquipmentType.ride_on],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v02", name="PHX Truck 2", crew_size=3, equipment=[EquipmentType.standard, EquipmentType.ride_on],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v03", name="PHX Truck 3", crew_size=2, equipment=[EquipmentType.standard],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v04", name="PHX Truck 4", crew_size=2, equipment=[EquipmentType.standard],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v05", name="PHX Tree Crew", crew_size=4, equipment=[EquipmentType.tree_service, EquipmentType.standard],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v06", name="PHX Irrigation Van", crew_size=2, equipment=[EquipmentType.irrigation],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v07", name="PHX Hardscape Rig", crew_size=4, equipment=[EquipmentType.hardscape, EquipmentType.standard],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
    Vehicle(id="phx-v08", name="PHX Truck 5", crew_size=3, equipment=[EquipmentType.standard, EquipmentType.ride_on],
            status=VehicleStatus.available, region=Region.phoenix, depot_id="depot-phx-1"),
]

# ── San Diego Region ──

SD_DEPOT = Depot(
    id="depot-sd-1",
    name="Verde SD Yard",
    location=Location(lat=32.8341, lng=-117.1447),
    region=Region.san_diego,
)

SD_PROPERTIES = [
    Property(id="sd-p01", name="La Jolla Village Square", address="8657 Villa La Jolla Dr, La Jolla, CA",
             location=Location(lat=32.8700, lng=-117.2232), property_type=PropertyType.retail, lot_acres=8.0, region=Region.san_diego),
    Property(id="sd-p02", name="Scripps Memorial Hospital", address="9888 Genesee Ave, La Jolla, CA",
             location=Location(lat=32.8800, lng=-117.2196), property_type=PropertyType.medical, lot_acres=6.0, region=Region.san_diego),
    Property(id="sd-p03", name="UTC Westfield", address="4545 La Jolla Village Dr, San Diego, CA",
             location=Location(lat=32.8698, lng=-117.2068), property_type=PropertyType.retail, lot_acres=25.0, region=Region.san_diego),
    Property(id="sd-p04", name="Sorrento Valley Business Park", address="5985 Pacific Center Blvd, San Diego, CA",
             location=Location(lat=32.8990, lng=-117.1975), property_type=PropertyType.commercial, lot_acres=10.0, region=Region.san_diego),
    Property(id="sd-p05", name="Torrey Pines Science Park", address="10996 Torreyana Rd, San Diego, CA",
             location=Location(lat=32.8985, lng=-117.2330), property_type=PropertyType.commercial, lot_acres=12.0, region=Region.san_diego),
    Property(id="sd-p06", name="Mira Mesa Business Park", address="9325 Sky Park Ct, San Diego, CA",
             location=Location(lat=32.9120, lng=-117.1380), property_type=PropertyType.industrial, lot_acres=8.0, region=Region.san_diego),
    Property(id="sd-p07", name="Mira Mesa Town Center", address="8290 Mira Mesa Blvd, San Diego, CA",
             location=Location(lat=32.9150, lng=-117.1509), property_type=PropertyType.retail, lot_acres=6.0, region=Region.san_diego),
    Property(id="sd-p08", name="Rancho Bernardo Town Center", address="11896 Bernardo Plaza Dr, San Diego, CA",
             location=Location(lat=33.0126, lng=-117.0770), property_type=PropertyType.retail, lot_acres=10.0, region=Region.san_diego),
    Property(id="sd-p09", name="RB Community Park HOA", address="18448 W Bernardo Dr, San Diego, CA",
             location=Location(lat=33.0213, lng=-117.0867), property_type=PropertyType.hoa, lot_acres=15.0, region=Region.san_diego),
    Property(id="sd-p10", name="Palomar Medical Center", address="15615 Pomerado Rd, Poway, CA",
             location=Location(lat=32.9794, lng=-117.0427), property_type=PropertyType.medical, lot_acres=7.0, region=Region.san_diego),
    Property(id="sd-p11", name="Carmel Mountain Ranch HOA", address="11588 Carmel Mountain Rd, San Diego, CA",
             location=Location(lat=32.9754, lng=-117.0783), property_type=PropertyType.hoa, lot_acres=20.0, region=Region.san_diego),
    Property(id="sd-p12", name="Scripps Ranch Business Park", address="10179 Huennekens St, San Diego, CA",
             location=Location(lat=32.9031, lng=-117.1105), property_type=PropertyType.commercial, lot_acres=5.0, region=Region.san_diego),
    Property(id="sd-p13", name="Poway Municipal Complex", address="13325 Civic Center Dr, Poway, CA",
             location=Location(lat=32.9582, lng=-117.0373), property_type=PropertyType.municipal, lot_acres=4.0, region=Region.san_diego),
    Property(id="sd-p14", name="Del Mar Heights Office Park", address="12625 High Bluff Dr, San Diego, CA",
             location=Location(lat=32.9338, lng=-117.2283), property_type=PropertyType.commercial, lot_acres=6.0, region=Region.san_diego),
    Property(id="sd-p15", name="Sabre Springs Business Park", address="13280 Evening Creek Dr, San Diego, CA",
             location=Location(lat=32.9587, lng=-117.0927), property_type=PropertyType.industrial, lot_acres=9.0, region=Region.san_diego),
]

SD_VEHICLES = [
    Vehicle(id="sd-v01", name="SD Truck 1", crew_size=3, equipment=[EquipmentType.standard, EquipmentType.ride_on],
            status=VehicleStatus.available, region=Region.san_diego, depot_id="depot-sd-1"),
    Vehicle(id="sd-v02", name="SD Truck 2", crew_size=3, equipment=[EquipmentType.standard, EquipmentType.ride_on],
            status=VehicleStatus.available, region=Region.san_diego, depot_id="depot-sd-1"),
    Vehicle(id="sd-v03", name="SD Truck 3", crew_size=2, equipment=[EquipmentType.standard],
            status=VehicleStatus.available, region=Region.san_diego, depot_id="depot-sd-1"),
    Vehicle(id="sd-v04", name="SD Tree Crew", crew_size=4, equipment=[EquipmentType.tree_service, EquipmentType.standard],
            status=VehicleStatus.available, region=Region.san_diego, depot_id="depot-sd-1"),
    Vehicle(id="sd-v05", name="SD Irrigation Van", crew_size=2, equipment=[EquipmentType.irrigation],
            status=VehicleStatus.available, region=Region.san_diego, depot_id="depot-sd-1"),
]


def get_depot(region: Region) -> Depot:
    return PHX_DEPOT if region == Region.phoenix else SD_DEPOT


def get_properties(region: Region) -> list[Property]:
    return PHX_PROPERTIES if region == Region.phoenix else SD_PROPERTIES


def get_vehicles(region: Region) -> list[Vehicle]:
    return PHX_VEHICLES if region == Region.phoenix else SD_VEHICLES
