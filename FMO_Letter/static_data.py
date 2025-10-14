FIELD_SPECS = {
    'LETTER_IND': 2,               # PIC X(02)
    'TEXT_IND': 2,                 # PIC X(02)
    'CONTRACT_NUMBER': 9,          # PIC Z99999999. (9 positions)
    'COPY_IND': 1,
    'CYCLE_DATE': 8,               # PIC 9(8)
    'ANNUITANT_NAME': 60,          # PIC X(60)
    'CONTRACT_OWNER_NAME': 60,     # PIC X(60)
    'REPRESENT_NAME': 60,          # PIC X(60)
    'PHONE_NUMBER': 14,            # PIC X(14)
    'AGENT_CODE': 12,              # PIC X(12)
    'MAIL_ADDRESSEE_NAME': 38,     # PIC X(38)
    'ADDRESSEE_LINE1': 38,         # PIC X(38)
    'ADDRESSEE_LINE2': 38,         # PIC X(38)
    'ADDRESSEE_LINE3': 38,         # PIC X(38)
    'CITY_STATE_ZIP_CODE': 32,     # PIC X(32)
    'COMPANY_CODE': 3,             # PIC X(03)
    'PLAN_MARKET_NAME': 50,        # PIC X(50)
    # Dynamic fields
    'FMO_MATURE_YEAR': 4,          # PIC X(4)
    'FMO_MATURE_DATE': 8,          # PIC 9(8)
    'FMO_MATURE_VALUE': 13,        # PIC X(13)
    'FMO_RETURN_DATE': 8,          # PIC 9(8)
    'FMO_AGENT_NAME': 50,          # PIC X(50)
    'FMO_CC_NAME': 50,             # PIC X(50)
    'NUMBER_OF_FUNDS': 3,          # PIC X(03)
    'RETURN_BY_MMDD': 8,           # PIC 9(8)
    'EARLIEST_FMO': 50,            # PIC X(50)
    'EARLIEST_RATE': 4,            # PIC Z9.99 -> allocate 4 chars (eg '4.50')
}


title = "F M O  M A T U R I T Y   N O T I C E"

company_names = {
    "": "Equitable Financial Life Insurance Company",
    "EQC": "Equitable Financial Life Insurance Company",
    "EFA": "Equitable Financial Life Insurance Company of America",
    "EFC": "Equitable Financial Life and Annuity Company",
}

notice_info = {
    '0':["""Our records indicate that a portion of your above referenced Accumulator Series variable annuity contract/certificate
         is invested in the [FMO_MATURE_YEAR] Fixed Maturity Option (FMO). Your contract/certificate may refer to the FMOs as Guarantee
         Periods. Your [FMO_MATURE_YEAR] FMO is scheduled to mature on [FMO_MATURE_DATE] with a maturity value of [FMO_MATURE_VALUE] on that date.,        
         """],   
    
    '1':[
        """As of June 30, 2022, we will no longer accept new allocations or reinvestment instructions to FMOs. You may choose to
        reinvest the value of this FMO at maturity among any or all of the investment options then available under your
        contract/certificate. You may also withdraw these funds. Withdrawals may be subject to a contingent withdrawal
        charge, may be subject to income tax and may be subject to an additional federal income tax penalty if you are younger
        than 59 and one-half.
        """],
    
    '2':["""We must receive your instructions with respect to the maturing FMO at our Processing Office by [FMO-RETURN-DATE].
         Please complete and return the enclosed form by that date. Accordingly, if we do not hear from you, the maturing funds
         will be reinvested into the EQ/Money Market."""],
    
    '3':["""If you have any questions, please call your financial professional, [FMO-AGENT-NAME], or our Service Center at 1 -800-789-7771 ."""],
    '4':["""Sincerely,"""],
    '5':["""Retirement Service Solutions"""],
    '6':["""cc: Wayne Curtis, ChFC, CLU"""],
    '7':["""Income Manager Annuities are issued by Equitable Life Insurance Company"""],
    '8':["""and are distributed by EQUITABLE Distributors, LLC."""],
    
}

assistance_msg = "If you need assistance, please call your representative at the phone <br/>" \
                 "number above, or call our processing office toll free at 1-800-789-7771, <br/>" \
                 "or visit our website at www.equitable.com."                    


fundlist_notice = {
    '0': ["""INCOME MANAGER FIXED MATURITY OPTIONS"""],

    '1': ["""____ I elect to have the maturity value of my expiring FMO reinvested as follows:
             (Please indicate dollar amounts or percentages. Percentages should equal 100%.)"""],

    '2': ["""<<Fundlist>>"""],

    '3': ["""____ I elect to have the maturity value of my expiring FMO distributed to me as a withdrawal.
                  (Distributions are a taxable event, and may be subject to withdrawal charges and an additional 10% federal income tax penalty.)"""],

    '4': ["""WITHHOLDING INSTRUCTIONS:"""],

    '5': ["""___ A. I do not want federal income tax withheld. (U.S. residence and Social Security number required)
___ B. I want 10% federal income tax withheld from the taxable amount of this distribution.
___ C. U.S. Resident: ___Yes ___No"""],

    '6': ["""____________________________________     _________________________
Signature of owner                       Date"""],

    '7': ["""____________________________________
Social Security Number"""], 

    '8': ["""Return to: Equitable
500 Plaza Drive
6th Floor
Secaucus, NJ 07094"""],     
}
