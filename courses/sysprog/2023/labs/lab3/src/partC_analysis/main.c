#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <arpa/inet.h>
#include "packetProcess.h"
#include "filter.h"

int main(){
    int PACKET_LEN = 16000;
    int PACKET_AMOUNT = 1000;
    unsigned char buffer[PACKET_LEN];
    struct sockaddr saddr;
    struct packet_mreq mr;

    // create a row socket
    int sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if(sock < 0){
        printf("error in creating socket.\n");
        return -1;
    }

    // turn on the promiscuous mode
    mr.mr_type = PACKET_MR_PROMISC;
    setsockopt(sock, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr));

    printf("Start sniffing...\n");
    int count = 0;
    while(1){
        if(count > PACKET_AMOUNT)
            break;

        int saddr_len = sizeof saddr;
        int data_size = recvfrom(sock, buffer, PACKET_LEN, 0,
                                 &saddr, (socklen_t*)&saddr_len);

        if(data_size > 0){
            if(filterByProtocol(buffer, 2)){
                packet_process(buffer, data_size);
            }
        }else{
            printf("error in recvfrom func\n");
            return -1;
        }
    }

    count++;
    close(sock);
    return 0;
}
