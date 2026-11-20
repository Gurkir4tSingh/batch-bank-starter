import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * STEP030 POST: apply data/valid.dat to the account balances in data/master_in.dat
 * and write the result to data/master.dat.
 *
 * Return codes: 0 ok, 4 warning (something was skipped), 8 error (a file could not be read or written).
 *
 * STARTER STATUS (on purpose, these are tickets):
 *   - deposits (D) and withdrawals (W) are posted
 *   - transfers (T) are NOT posted yet ................ ticket JAV-2
 *   - a withdrawal can push a balance below zero ...... ticket JAV-3
 */
public class Step030Post {
    static final Path DATA = Paths.get("data");

    public static void main(String[] args) {
        System.exit(run());
    }

    static int run() {
        Map<String, Long> balances = new LinkedHashMap<>();
        List<String> masterLines;
        List<String> validLines;
        try {
            masterLines = Files.readAllLines(DATA.resolve("master_in.dat"));
            validLines = Files.readAllLines(DATA.resolve("valid.dat"));
        } catch (IOException e) {
            System.out.println("POST      cannot read " + e.getMessage());
            return 8;
        }

        for (String line : masterLines) {
            if (line.isEmpty()) {
                continue;
            }
            try {
                balances.put(line.substring(0, 8), Long.parseLong(line.substring(8, 19)));
            } catch (RuntimeException e) {
                System.out.println("POST      bad master record: " + line);
                return 8;
            }
        }

        int posted = 0;
        int skipped = 0;
        for (String line : validLines) {
            if (line.isEmpty()) {
                continue;
            }
            Transaction t;
            try {
                t = Transaction.parse(line);
            } catch (IllegalArgumentException e) {
                skipped++;          // could not be read, so it cannot be posted
                continue;
            }
            Long balance = balances.get(t.getAcct());
            if (balance == null) {
                skipped++;          // unknown account
                continue;
            }

            switch (t.getType()) {
                case 'D':
                    balances.put(t.getAcct(), balance + t.getAmountCents());
                    posted++;
                    break;

                case 'W':
                    // TODO (JAV-3): if this would make the balance negative, skip it, count it, and return RC 4
                    balances.put(t.getAcct(), balance - t.getAmountCents());
                    posted++;
                    break;

                case 'T':
                    // TODO (JAV-2): post a transfer out as a withdrawal
                    break;

                default:
                    skipped++;      // unknown type
            }
        }

        StringBuilder out = new StringBuilder();
        for (Map.Entry<String, Long> e : balances.entrySet()) {
            out.append(e.getKey()).append(String.format(Locale.ROOT, "%011d", e.getValue())).append('\n');
        }
        try {
            Files.writeString(DATA.resolve("master.dat"), out.toString());
        } catch (IOException e) {
            System.out.println("POST      cannot write " + e.getMessage());
            return 8;
        }

        System.out.println("POST      " + posted + " posted, " + skipped + " skipped");
        return skipped > 0 ? 4 : 0;
    }
}
