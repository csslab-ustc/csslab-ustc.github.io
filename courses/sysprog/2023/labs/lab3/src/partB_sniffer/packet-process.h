#ifndef MINIWIRESHARK_PACKETPROCESS_H
#define MINIWIRESHARK_PACKETPROCESS_H

// 包含对包的打印和计数所需的函数
// print
void packet_print(unsigned char *buffer, int buffer_len);

// print format of etherNet-header
void mac_header(unsigned char *buffer, int buffer_len);

// print format of ip-header
void ip_header(unsigned char *buffer, int buffer_len);

// printf format of arp-header
void arp_header(unsigned char *buffer, int buffer_len);

// print format of tcp-header
void tcp_header(unsigned char *buffer, int buffer_len);

// print format of udp-header
void udp_header(unsigned char *buffer, int buffer_len);

// print format of icmp-header
void icmp_header(unsigned char *buffer, int buffer_len);

// print format of payload
void payload(unsigned char *buffer,int buffer_len);

// print TCP packet
void TCP_printer(unsigned char *buffer, int buffer_len);

// print UDP packet
void UDP_printer(unsigned char *buffer, int buffer_len);

// print ARP packet
void ARP_printer(unsigned char *buffer, int buffer_len);

// packet process func
void packet_process(unsigned char *buffer, int buffer_len);

#endif //MINIWIRESHARK_PACKETPROCESS_H