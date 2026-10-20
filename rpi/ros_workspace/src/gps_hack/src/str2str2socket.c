#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int
main()
{

  // this will fail if the ublox link does not exist
  setbuf(stdout,NULL);
  setbuf(stderr,NULL);
  char ubloxDev[]="/ublox";
  char str2str[128];
  char sed[128];
  char grep[128];
  char cut[64];
  sprintf(cut,"cut -f 2-5 -d ,");
  sprintf(grep,"stdbuf -o 0 grep -a 'GNGLL'");
  sprintf(str2str,"stdbuf -o 0 str2str -in serial:/%s:9600:8:n:1:off 2>/dev/null",ubloxDev);
  sprintf(sed,"stdbuf -o 0 sed -e 's/\\r//'");
  char theCommand[1024];
  sprintf(theCommand,"%s | %s | %s | %s",str2str,grep,sed,cut);
  FILE *pipe=popen((const char *)theCommand,"w");

  while(!feof(pipe)) {
    char line[1024];
    //fscanf(pipe,"%s\n",line);
    int inch=fgetc(pipe);
    fputc(inch,pipe);
    //printf("%s\n",line);
  }

  

  //printf("%s\n",theCommand);
  //system(theCommand);
  //system("/home/belfore/bin/str2str -in serial://ttyACM1:9600:8:n:1:off 2>/dev/null | sed -e 's/\r//' | grep -a 'GNGLL'| sed -e 's///' ");
}
// stdbuf -o 0 /home/belfore/bin/str2str -in serial://ttyACM1:9600:8:n:1:off 2>/dev/null    | stdbuf -o 0 grep -a GNGLL | stdbuf -o 0 sed -e 's/^M//'
