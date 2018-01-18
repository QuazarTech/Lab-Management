// g++ -pthread -Wall -O3 -std=c++14 test.cxx -o test -lL412B -lftdi

// QDAL41xB specific driver libraries
#include <L412B/driver/include/Driver.h>

// LiveData datastructure defined here
#include <L412B/driver/include/Data.h>

// Standard libraries
#include <vector>
#include <iostream>
#include <typeinfo>
#include <string>
#include <fstream>
#include <iomanip>
//#include <cstdlib>
//#include <memory>
using namespace std;

// Constant definitions
#define SMOKE_SENS_THRESHOLD 0.7
#define TEMP_SENS_THRESHOLD 115.0

#define PRINT_PRECISION 8

void send_alert (int channel);
void add_status_to_email (std::string status);

int main (void)
{

    // Scan for list of QDAL41xB devices connected
	auto device_list = L412B::Driver::scan();

    // Terminate program if no QDAL41xB device found
	if (device_list.empty())
	{
		std::cout << "No QDA device found." << std::endl;
		return (-1);
	}

    // Get the Serial number of the first QDAL41xB device found
    // All subsequent instructions for data acquisition will refer to this QDAL41xB device
	auto serialNo = device_list[0].serialNo();
	std::cout << "Serial No:" << serialNo <<std::endl;

    // Create a new instance of QDAL41xB driver and wraps it in a unique_ptr
    auto driver = std::make_unique<L412B::Driver>();
    std::cout << "driver type is " << typeid(driver).name() << std::endl;

    // Connect to QDAL41xB device
    driver->connect (serialNo);

    // Start acquiring data from the QDAL41xB
	driver->start_acquisition ();


    while(1)
    {
        // Stream collected data from the QDAL41xB device
        auto live_data = driver->live_data();

        /* live_data is a std::vector<data::LiveData>
         * LiveData is defined in driver/include/Data.h
         * LiveData.time() : Returns the time axis value (double) of the data
         * LiveData.chn() : QDAL41xB channel (int) where the data originated
         * LiveData.data() : Returns the data value (float)
         * LiveData.logical_chn() : float /Use : TODO/
         */

        // Keep polling until data is available
        if (live_data.empty()) continue;


        // If data is available, check for threshold violations
        for (unsigned int i = 0; i < live_data.size(); i++)
        {
            // Checking data points spaced 1 second apart
            double intpart = 0.0;

            // Compare fractional part of time to zero
            if (std::modf (live_data[i].time() * 1.0, &intpart) == 0.00)
            {
                // Data for Channel-1 (Smoke Sensor)
                if (live_data[i].chn() == 0)
                {
                    // Display data on terminal
                    std::cout << std::setprecision(PRINT_PRECISION) <<  "Time : \a" << live_data[i].time() << "\t Chn 1:  " << live_data[i].data() << "\t";

                    // Alert if signal is above threshold
                    if (live_data[i].data() > SMOKE_SENS_THRESHOLD)
                    {
                        send_alert (live_data[i].chn());
                        break;
                    }

                }

                // Data for Channel-2 (Smoke Sensor)
                if (live_data[i].chn() == 1)
                {
                    std::cout << std::setprecision(PRINT_PRECISION) << "Time : \a" << live_data[i].time() << "\t Chn 2:  " << live_data[i].data() << std::endl;

                    // Alert if signal is above threshold
                    if (live_data[i].data() > SMOKE_SENS_THRESHOLD)
                    {
                        send_alert (live_data[i].chn());
                        break;
                    }

                }

                // Data for Channel-3 (Temperature Sensor)
                if (live_data[i].chn() == 2)
                {
                    std::cout << std::setprecision(PRINT_PRECISION) << "Time : \a" << live_data[i].time() << "\t Chn 3:  " << live_data[i].data() << "\t";

                    // Alert if signal is above threshold
                    if (live_data[i].data() > TEMP_SENS_THRESHOLD)
                    {
                        send_alert (live_data[i].chn());
                        break;
                    }

                }

                // Data for Channel-4 (Temperature Sensor)
                if (live_data[i].chn() == 3)
                {
                    std::cout << std::setprecision(PRINT_PRECISION) << "Time : \a" << live_data[i].time() << "\t Chn 4:  " << live_data[i].data() << "\n" << std::endl;

                    // Alert if signal is above threshold
                    if (live_data[i].data() > TEMP_SENS_THRESHOLD)
                    {
                        send_alert (live_data[i].chn());
                        break;
                    }
                }

            }

        }

    } // while (1)

    // Stop acquisition
    driver->stop_acquisition ();

    // Disconnect QDAL41xB device
    driver->disconnect();

    return 0;

} // end main

void add_status_to_email (std::string status)
{
    // Open mail.txt to append data to end of file
    ofstream mail_file;
    mail_file.open ("mail.txt", ios::out | ios::app);

    if (mail_file.is_open())
    {
        mail_file << status;
        mail_file.close();
    }

    else
    {
        std::cout << "Unable to add alert status to mail." << std::endl;
    }


}

void send_alert (int channel)
{
    std::string status;

    switch (channel)
    {
        case 0 : status = "Smoke Sensor 1 : HIGH";
                 break;
        case 1 : status = "Smoke Sensor 2 : HIGH";
                 break;
        case 2 : status = "Temperature Sensor 1 : HIGH";
                 break;
        case 3 : status = "Temperature Sensor 2 : HIGH";
                 break;
        default : status = "Unknown Alert Message";
                 break;
    }

    // Display Alert status on terminal
    std::cout << "\n\n\t\t ****** DANGER ******" << std::endl;
    std::cout << "\nAlert Status" << std::endl;
    std::cout << "*********************" << std::endl;
    std::cout << status << "\n" << std::endl;

    // Update alert email with alert status
    add_status_to_email ("\n\nAlert Status\n");
    add_status_to_email ("*******************\n");
    add_status_to_email (status);

//     std::cout << "Sending alert mails..." << std::endl;
//     // Send email to gitansh@quazartech.com
//     system("ssmtp gitansh@quazartech.com < mail.txt");
//
//     // Send email to mani@quazartech.com
//     system("ssmtp mani@quazartech.com < mail.txt");
//
//     // Send email to kc@quazartech.com
//     system("ssmtp kc@quazartech.com < mail.txt");
//
//     // Send email to nishant@quazartech.com
//     system("ssmtp nishant@quazartech.com < mail.txt");

    std::cout << "\t \t Alert mails sent." << std::endl;
    system("aplay alarm.wav");
}