/**
 * One 26-character transaction record: ACCT(8) TYPE(1) AMOUNT(9, in cents) DATE(8).
 *
 * Example: ACCT0001D00001255020261120  =  account ACCT0001, deposit, $125.50, 2026-11-20
 */
public class Transaction {
    public static final int LENGTH = 26;

    private final String acct;
    private final char type;
    private final long amountCents;
    private final String date;

    public Transaction(String acct, char type, long amountCents, String date) {
        this.acct = acct;
        this.type = type;
        this.amountCents = amountCents;
        this.date = date;
    }

    /** Slice one fixed-width line into fields. Throws IllegalArgumentException if it cannot be read. */
    public static Transaction parse(String line) {
        if (line == null || line.length() != LENGTH) {
            throw new IllegalArgumentException("record is not " + LENGTH + " characters");
        }
        String amountText = line.substring(9, 18);
        for (int i = 0; i < amountText.length(); i++) {
            char c = amountText.charAt(i);
            if (c < '0' || c > '9') {
                throw new IllegalArgumentException("amount is not all digits: " + amountText);
            }
        }
        return new Transaction(
                line.substring(0, 8),
                line.charAt(8),
                Long.parseLong(amountText),
                line.substring(18, 26));
    }

    public String getAcct() {
        return acct;
    }

    public char getType() {
        return type;
    }

    public long getAmountCents() {
        return amountCents;
    }

    public String getDate() {
        return date;
    }

    public boolean isValidType() {
        return type == 'D' || type == 'W' || type == 'T';
    }
}
