DOCUMENT_RULES = {
    "agreement_of_assignment": {
        "required": [
            "assignor",
            "assignee",
            "consideration",
            "rights transferred",
            "governing law",
            "amount",
            "date",
            "signatures",
            "witness"
        ],
        "optional": ["indemnity", "termination", "stamp duty"]
    },

    "leave_and_licence": {
        "required": [
            "licensor",
            "licensee",
            "license fee",
            "duration",
            "property description",
            "termination",
            "deposit",
            "date",
            "signatures",
            "witness",
            "stamp duty"
        ],
        "optional": ["renewal clause", "registration"]
    },

    "sale_deed_agri": {
        "required": [
            "seller",
            "buyer",
            "sale consideration",
            "property details",
            "stamp duty",
            "registration",
            "amount",
            "date",
            "signatures",
            "witness"
        ]
    },

    "development_agreement": {
        "required": [
            "developer",
            "landowner",
            "project details",
            "revenue sharing",
            "approvals",
            "termination",
            "date",
            "signatures",
            "witness",
            "stamp duty"
        ]
    },

    "simple_mortgage": {
        "required": [
            "mortgagor",
            "mortgagee",
            "loan amount",
            "interest rate",
            "repayment terms",
            "default clause",
            "amount",
            "date",
            "signatures",
            "witness"
        ]
    },

    "transfer_deed_flat": {
        "required": [
            "transferor",
            "transferee",
            "flat details",
            "consideration",
            "society approval",
            "registration",
            "amount",
            "date",
            "signatures",
            "witness",
            "stamp duty"
        ]
    }
}