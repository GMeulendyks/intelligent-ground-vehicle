#include <stdio.h>
#include <math.h>
#include <string.h>

int
main()
{
  int inch;
  char buf[1024];
  const char *gngll="GNGLL";
  char fieldBusRev[strlen(gngll)+1];
  char tmp[strlen(gngll)+1];
  char fieldBus[strlen(gngll)+1];
  int i=0;
  for(i=0;i<strlen(gngll);i++) fieldBusRev[i]=0;
  fieldBusRev[i]=0;
  for(i=0;i<strlen(gngll);i++) fieldBus[i]=0;
  fieldBus[i]=0;
  while((inch=getc(stdin))!=EOF) {
    for(i=0;i<strlen(gngll)-1;i++) {
      tmp[i+1]=fieldBusRev[i];
    }
    tmp[0]=inch;
    strcpy(fieldBusRev,tmp);

    for(i=0;i<strlen(fieldBusRev);i++) {
      fieldBus[i]=fieldBusRev[strlen(gngll)-1-i];
    }
    // now reverse 
    /* for(i=strlen(gngll)-1;i>0;i--) { */
    /*   fieldBus[i]=fieldBus[i-1]; */
    /* } */
    /* fieldBus[0]=inch; */
    //printf("%s/%s\n",fieldBus,gngll);
    if(!strcmp(fieldBus,gngll)) {
      // found one
      // scan ahead to the first comma
      while((inch=getc(stdin))!=',');

      i=0;
      while((inch=getc(stdin))!='\r') {
        buf[i++]=inch;
      }
      buf[i]=0;
      printf("%s\n",buf);
      fflush(stdout);
      //$GNGLL,4240.09092,N,08313.03643,W,023548.00,A,D*63
    }
  }
}

