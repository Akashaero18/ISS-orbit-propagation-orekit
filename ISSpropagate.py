#Initializing orekit    
import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir 
setup_orekit_curdir()

from org.orekit.time import TimeScalesFactory , AbsoluteDate
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.frames import FramesFactory
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.utils import Constants, IERSConventions
import matplotlib.pyplot as plt
import numpy as np

def propagate_tle(tle_1, tle_2,start_time,duration_hrs, step_sec=120.0):
    ISStle = TLE(tle_1, tle_2)
    propagator = TLEPropagator.selectExtrapolator(ISStle)

    print("Epoch : ",ISStle.getDate())

    #Propagation Time range
    start_time = AbsoluteDate(start_time[0], start_time[1], start_time[2], start_time[3], start_time[4],
                              start_time[5], TimeScalesFactory.getUTC())
    end_time = start_time.shiftedBy(duration_hrs * 60.0 * 60.0)

    ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
    earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING,
                         ITRF)

    #Lists to store lats, lons and time

    lats = []
    lons = []
    alts = []
    times = []

    current_date = start_time

    while(current_date.compareTo(end_time) <= 0.0):

        # Propagatin to current time/date
        state = propagator.propagate(current_date)
        position = state.getPVCoordinates().getPosition()

        geodetic_point = earth.transform(position, state.getFrame(), current_date)
        lats.append(np.degrees(geodetic_point.getLatitude()))   
        lons.append(np.degrees(geodetic_point.getLongitude()))   
        alts.append(geodetic_point.getAltitude() / 1000)
        times.append(current_date.durationFrom(start_time) / 3600.0)
        current_date = current_date.shiftedBy(step_sec)

    return lats, lons, alts, times

if __name__ == "__main__":

    #Input (Two - Element Line)
    tle_1 = "1 25544U 98067A   26141.16510469  .00005835  00000+0  11282-3 0  9993"
    tle_2 = "2 25544  51.6328  73.8715 0007528  81.3651 278.8190 15.49291753567564"

    lats, lons, alts, times = propagate_tle(tle_1, tle_2,(2026,1,9,8,59,59.0), 24 ,step_sec= 60.0)

    fig,(ax1, ax2) = plt.subplots(1,2, figsize= (16,6))

    #plotting Altitude over Time
    ax1.plot(times, alts, color='tab:red', linewidth=1.5)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Altitude (km)')
    ax1.set_title('ISS Altitude')
    ax1.grid(True, linestyle = '--', alpha = 0.7)

    #plotting Ground track Latitude vs Longitude
    ax2.scatter(lons,lats, s=1,color = 'blue')
    ax2.set_xlabel('Longitude(degrees)')
    ax2.set_ylabel('Latitude(degrees)')
    ax2.set_title('ISS Ground Track (24hrs)')
    ax2.set_xlim([-180, 180])
    ax2.set_ylim([-90, 90])
    ax2.grid(True, linestyle = '--',alpha = 0.7)

    plt.tight_layout()
    plt.show()