/**
 * A tiny test harness with no libraries.
 * Run it with:   python run_tests.py
 */
public class TestRunner {
    static int passed = 0;
    static int failed = 0;

    static void check(String name, boolean condition) {
        if (condition) {
            passed++;
        } else {
            failed++;
            System.out.println("FAIL: " + name);
        }
    }

    public static void main(String[] args) {
        testParsesFields();
        testIsValidType();
        System.out.println("Java tests: " + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }

    static void testParsesFields() {
        Transaction t = Transaction.parse("ACCT0001D00001255020261120");
        check("account", t.getAcct().equals("ACCT0001"));
        check("type", t.getType() == 'D');
        check("amount in cents", t.getAmountCents() == 12550);
        check("date", t.getDate().equals("20261120"));
    }

    static void testIsValidType() {
        check("D is valid", new Transaction("ACCT0001", 'D', 100, "20261120").isValidType());
        check("W is valid", new Transaction("ACCT0001", 'W', 100, "20261120").isValidType());
        check("T is valid", new Transaction("ACCT0001", 'T', 100, "20261120").isValidType());
        check("X is invalid", !new Transaction("ACCT0001", 'X', 100, "20261120").isValidType());
    }
}
