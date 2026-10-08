"""Generates multi-day, multi-zone synthetic city datasets across five domains."""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils.config import DATA_DIR, ZONES

def generate_all_datasets(days: int = 7, seed: int = 42):
    np.random.seed(seed)
    end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time, freq="h")

    traffic_records = []
    energy_records = []
    water_records = []
    waste_records = []
    air_records = []

    for zone in ZONES:
        zone_mult = {
            "Zone A": 1.4,
            "Zone B": 1.2,
            "Zone C": 1.0,
            "Zone D": 0.8,
            "Zone E": 0.6,
        }.get(zone, 1.0)

        for ts in timestamps:
            hour = ts.hour
            is_weekend = ts.weekday() >= 5

            # Traffic: Morning & Evening Commute Peaks
            m_peak = np.exp(-((hour - 8.5) ** 2) / 4.0)
            e_peak = np.exp(-((hour - 17.5) ** 2) / 5.0)
            commute = 1.0 + 1.6 * (m_peak + e_peak) if not is_weekend else 1.0 + 0.6 * np.exp(-((hour - 14) ** 2) / 8.0)
            
            base_vol = 750 * zone_mult * commute
            vehicle_count = int(np.clip(np.random.normal(base_vol, base_vol * 0.1), 80, 2600))
            norm_vol = min(vehicle_count / (2200 * zone_mult), 1.0)
            avg_speed = float(np.clip(60.0 * (1.0 - 0.7 * norm_vol) + np.random.normal(0, 2), 8.0, 75.0))
            travel_time = round(12.0 * (50.0 / avg_speed), 1)
            idle_time = round(max(0.0, (travel_time - 12.0) * 0.75 + np.random.uniform(0.5, 2.0)), 1)
            
            cong_lvl = "High" if (norm_vol > 0.75 or avg_speed < 22) else "Medium" if norm_vol > 0.45 else "Low"

            traffic_records.append({
                "zone_id": zone,
                "road_id": f"{zone[:4].upper()}-RD-{np.random.randint(1, 4)}",
                "timestamp": ts,
                "vehicle_count": vehicle_count,
                "average_speed": round(avg_speed, 1),
                "congestion_level": cong_lvl,
                "travel_time": travel_time,
                "idle_time": idle_time
            })

            # Energy: Afternoon Commercial & Evening Residential Peaks
            work_factor = 1.0 + 1.1 * np.exp(-((hour - 14) ** 2) / 12.0) if not is_weekend else 1.0 + 0.3 * np.exp(-((hour - 15) ** 2) / 10.0)
            base_elec = 4200 * zone_mult * work_factor
            elec_val = float(np.clip(np.random.normal(base_elec, base_elec * 0.08), 500, 15000))
            solar_peak = max(0.0, np.sin((hour - 6) / 12.0 * np.pi)) if 6 <= hour <= 18 else 0.0
            renewable_gen = round(elec_val * 0.32 * solar_peak + np.random.uniform(10, 80), 1)
            peak_demand = round(elec_val * np.random.uniform(1.15, 1.30), 1)
            eff_idx = round(np.clip((renewable_gen / (elec_val + 1e-5)) * 100 + 40 - (elec_val / 200), 20.0, 95.0), 1)

            energy_records.append({
                "zone_id": zone,
                "building_id": f"{zone[:4].upper()}-BLD-01",
                "timestamp": ts,
                "electricity_consumption": round(elec_val, 1),
                "peak_demand": peak_demand,
                "renewable_generation": renewable_gen,
                "energy_efficiency_indicator": eff_idx
            })

            # Water: Diurnal Rhythms with Pressure Dynamics
            w_m = np.exp(-((hour - 7.5) ** 2) / 3.0)
            w_e = np.exp(-((hour - 19.5) ** 2) / 4.0)
            water_factor = 0.5 + 1.2 * (w_m + w_e)
            baseline = 6800 * zone_mult * water_factor
            consumption = float(np.clip(np.random.normal(baseline, baseline * 0.07), 800, 18000))
            flow_val = round(consumption / 3600.0 * 2.8, 2)
            pressure = round(np.clip(4.2 - (flow_val / 12.0) + np.random.normal(0, 0.1), 1.8, 5.0), 2)

            water_records.append({
                "zone_id": zone,
                "building_id": f"{zone[:4].upper()}-WTR-MAIN",
                "timestamp": ts,
                "water_consumption": round(consumption, 1),
                "water_flow": flow_val,
                "pressure": pressure,
                "historical_average": round(baseline, 1)
            })

            # Waste Generation & Periodic Collection
            gen_base = 320 * zone_mult * (1.3 if is_weekend else 0.95) * (0.8 + 0.4 * np.sin(hour / 4))
            waste_gen = float(np.clip(np.random.normal(gen_base, 35), 40, 1200))
            cap = 1100 * zone_mult
            coll_val = round(waste_gen * np.random.uniform(0.75, 0.98), 1) if hour in [6, 14, 22] else 0.0

            waste_records.append({
                "zone_id": zone,
                "timestamp": ts,
                "waste_generated": round(waste_gen, 1),
                "waste_collected": coll_val,
                "waste_type": "Mixed Municipal",
                "collection_capacity": round(cap, 1),
                "collection_frequency": "3x Daily"
            })

            # Air Quality: Emissions Correlated with Vehicle Traffic & Idle Time
            inv_factor = 1.3 if (hour <= 7 or hour >= 21) else 0.9
            traffic_impact = (vehicle_count / 1800.0) * (idle_time / 6.0)
            pm25 = float(np.clip(18.0 + 24.0 * traffic_impact * inv_factor + np.random.normal(0, 3), 5.0, 220.0))
            pm10 = round(pm25 * np.random.uniform(1.4, 1.85), 1)
            co2 = round(390.0 + 85.0 * traffic_impact + np.random.normal(0, 8), 1)
            no2 = round(16.0 + 38.0 * traffic_impact + np.random.normal(0, 4), 1)
            aqi = int(max(pm25 * 2.1, no2 * 1.6, pm10 * 0.95))

            air_records.append({
                "zone_id": zone,
                "timestamp": ts,
                "PM2_5": round(pm25, 1),
                "PM10": pm10,
                "CO2": co2,
                "NO2": no2,
                "AQI": aqi
            })

    pd.DataFrame(traffic_records).to_csv(DATA_DIR / "traffic.csv", index=False)
    pd.DataFrame(energy_records).to_csv(DATA_DIR / "energy.csv", index=False)
    pd.DataFrame(water_records).to_csv(DATA_DIR / "water.csv", index=False)
    pd.DataFrame(waste_records).to_csv(DATA_DIR / "waste.csv", index=False)
    pd.DataFrame(air_records).to_csv(DATA_DIR / "air_quality.csv", index=False)
    print(f"Generated realistic synthetic city dataset across {len(ZONES)} zones and {days} days.")

if __name__ == "__main__":
    generate_all_datasets()