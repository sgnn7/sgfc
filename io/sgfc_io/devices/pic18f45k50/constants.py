PIC_REGISTER = {
    'INTCON': 0xf2,
    'INTCON2': 0xf1,
    'INTCON3': 0xf0,

    'SSP1CON3': 0xcb,
    'SSP1MSK': 0xca,
    'SSP1BUF': 0xc9,
    'SSP1ADD': 0xc8,
    'SSP1STAT': 0xc7,

    'SSP1CON1': 0xc6,
    'SSP1CON2': 0xc5,

    'TMR2': 0xbc,
    'T2CON': 0xba,

    'PSTR1CON': 0xb9,
    'BAUDCON1': 0xb8,
    'PWM1CON': 0xb7,
    'SPBRGH1': 0xb0,

    'TRISE': 0x96,
    'TRISD': 0x95,
    'TRISC': 0x94,
    'TRISB': 0x93,
    'TRISA': 0x92,

    'LATA': 0x89,
    'LATB': 0x8a,
    'LATC': 0x8b,
    'LATD': 0x8c,
    'LATE': 0x8d,

    'PORTA': 0x80,
    'PORTB': 0x81,
    'PORTC': 0x82,
    'PORTD': 0x83,
    'PORTE': 0x84,

    'ANSELA': 0x5b,
    'ANSELB': 0x5c,
    'ANSELC': 0x5d,
    'ANSELD': 0x5e,
    'ANSELE': 0x5f,

    'GP_RAM1': 0x52,
    'GP_RAM2': 0x51,
    'GP_RAM3': 0x50,
    'GP_RAM4': 0x4f,

    'SPBRG1': 0xaf,
    'CCPTMRS': 0x59,
    'CCP1CON': 0xbd,
    'CCPR1H': 0xbf,
    'CCPR1L': 0xbe,

    'T2CON': 0xba,
    'PR2': 0xbb,

    'VREFCON0': 0x7d,
    'VREFCON1': 0x7c,
    'VREFCON2': 0x7b,

    'ADCON0':  0xc2,
}

PIC_BITS = {
    'SSP1STAT_SMP': 7,
    'SSP1STAT_CKE': 6,
    'SSP1STAT_BF': 0,

    'SSP1CON1_WCOL': 7,
    'SSP1CON1_SSPOV': 6,
    'SSP1CON1_SSPEN': 5,
    'SSP1CON1_CKP': 4,

    'VREFCON1_DACEN': 7,
    'VREFCON1_DACLPS': 6,
    'VREFCON1_DACOE': 5,
    'VREFCON1_DACNSS': 0,
    'VREFCON1_DACPSS1': 3,
    'VREFCON1_DACPSS0': 2,
}
