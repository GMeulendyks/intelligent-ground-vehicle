#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <stdio.h>
#include <cstdlib>

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
//#include <sensor_msgs/msg/nav_sat_fix.hpp>
#include <geometry_msgs/msg/vector3.hpp>
//#include "odu_gps_msgs/msg/odu_fix.hpp"
//#include <odu_gps_msgs/msg/nav_sat_fix.hpp>

#ifndef UBLOX_PROCESSOR
#error Need to set UBLOX_PROCESSOR define.
#endif

using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class gps_talker : public rclcpp::Node
{
public:
  gps_talker()
    : Node("gps_talker"), count_(0)
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("gps_string", 10);
    //fix_ =       this->create_publisher<sensor_msgs::msg::NavSatFix>("odufix", 10);
    const std::string topic="/odu/fix";

    //publisher_ =     this->create_publisher<std_msgs::msg::String>("gps_string", 10);
    odu_fix_ =       this->create_publisher<geometry_msgs::msg::Vector3>(topic,10);
    timer_ = this->create_wall_timer(500ms, std::bind(&gps_talker::timer_callback, this));
    this->initializePipe();
  }

  // want to publish new message every time we receive a new line from the GPS
private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello, world! " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  //rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr fix_;
  rclcpp::Publisher<geometry_msgs::msg::Vector3>::SharedPtr odu_fix_;

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;

  void
  initializePipe()
  {
    //printf("running gps_hack.sh");
    const char *home=getenv("HOME");
    printf("home=%s\n",home);
    const char *colcon_prefix_path=getenv("COLCON_PREFIX_PATH");
    char ws_root[128];
    int slashes=0;
    for(int j=0;j<strlen(colcon_prefix_path);j++) {
      if(colcon_prefix_path[j]=='/') slashes++;
    }
    int slashCount=0;
    for(int j=0;j<strlen(colcon_prefix_path);j++) {
      if(colcon_prefix_path[j]=='/') slashCount++;
      if(slashCount==(slashes)) {
        ws_root[j]=0;
      } else {
        ws_root[j]=colcon_prefix_path[j];
      }
    }
    printf("ws_root=%s\n",ws_root);
    // the following assumes the gps_hack package is in the ws src folder
    const char *gps_hack_src_path="src/gps_hack/src";
    
    //char ubloxDev[]="/ublox";
    char ubloxDev[]="/ttyACM0";
    //char ubloxDev[]="/ttyACM1";
    char str2str[128];
    char sed[128];
    char grep[128];
    char cut[64];
    sprintf(cut,"cut -f 2-5 -d ,");
    sprintf(grep,"stdbuf -o 0 grep -a 'GNGLL'");
    sprintf(str2str,"stdbuf -o 0 str2str -in serial:/%s:9600:8:n:1:off ",ubloxDev);
    //sprintf(str2str,"stdbuf -o 0 /home/belfore/bin/str2str -in serial:/%s:9600:8:n:1:off 2>/dev/null",ubloxDev);
    sprintf(sed,"stdbuf -o 0 sed -e 's/\\r//'");
    char theCommand[1024];
     // const char *theShellCommand=UBLOX_PROCESSOR;
     char shellCommand[256];
     sprintf(shellCommand,"%s",UBLOX_PROCESSOR);
     printf("shellCommand=%s\n",shellCommand);
     
   sprintf(theCommand,"( %s | %s )",str2str,shellCommand);
    //sprintf(theCommand,"( %s | %s | %s | %s )",str2str,grep,sed,cut);
    //printf("%s\n",theCommand);
    //const char *theShellCommand="/home/belfore/ros2_ws/src/gps_hack/src/ublox_processor";
    //printf("running gps_hack.sh");
    fflush(stdout);
    //FILE *pipe=popen((const char *)theCommand,"w");
    FILE *pipe=popen(theCommand,"r");

    int i=0;
      char line[1024];
    while(!feof(pipe)) {
      //printf("tol\n");
      //fscanf(pipe,"%s\n",line);
      int inch=fgetc(pipe);
      if(inch=='\n') {
        if(line[0]!=',') {
          auto message = std_msgs::msg::String();
          double lat,lon;
          char latStr[32],lonStr[32];
          char N,W;
          for(i=0;i<strlen(line);i++) if(line[i]==',') line[i]=' ';
          sscanf(line,"%s %c %s %c",latStr,&N,lonStr,&W);
          message.data = line;
          //printf("lat=%s, N=%c lon=%s W=%c\n",latStr,N,lonStr,W);
          int latDeg,latMin;
          int lonDeg,lonMin;
          latDeg=(latStr[0]-'0')*10+latStr[1]-'0';
          latMin=(latStr[2]-'0')*10+latStr[3]-'0';
          // lonStr has a leading zero
          lonDeg=(lonStr[1]-'0')*10+lonStr[2]-'0';
          lonMin=(lonStr[3]-'0')*10+lonStr[4]-'0';
          double latMinFrac,lonMinFrac;
          sscanf(latStr+4,"%lf",&latMinFrac);
          sscanf(lonStr+5,"%lf",&lonMinFrac);
          double latVal,lonVal;
         
          latVal=latDeg+(latMin+latMinFrac)/60;
          lonVal=lonDeg+(lonMin+lonMinFrac)/60;
         if(N!='N') latVal=-latVal;
          if(W=='W') lonVal=-lonVal;
          //printf("lat/lon=(%12.8lf,%12.8lf)\n",latVal,lonVal);
          publisher_->publish(message);
           auto fix = geometry_msgs::msg::Vector3();
           fix.x=latVal; fix.y=lonVal;fix.z=0;
         odu_fix_->publish(fix);
        } // comma indicates loss of GPS fix
        i=0;
      } else {
        //if(isalpha(inch)) {
            line[i++]=inch;
            line[i]=0;
            //printf("%s\n",line);
            if(i>=1024) {
              printf("buffer issue\n");
              break;
            }
            //}
      }
      //fputc(inch,pipe);
      //printf("%s\n",line);
    }
    //printf("exited loop\n");
  }
  
  FILE *pipe;
  
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<gps_talker>());
  rclcpp::shutdown();
  return 0;
}
