package com.derits.multiselect;

import com.derits.multiselect.Log;
import com.derits.multiselect.UserHistory;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;

public class Main {

    public static void main(String[] args) throws Exception {
        List<Log> logs = loadLogs();
        System.out.println("Total logs count: " + logs.size());

        Collection<UserHistory> histories = convertToHistories(logs);
        System.out.println("User histories count: " + histories.size());

        long multiSearchUsersCount = histories.stream()
                .filter(UserHistory::hasMultiSearch)
                .count();

        System.out.printf(
                "Multi-search users count: %d (%.2f%%)%n",
                multiSearchUsersCount,
                ((double) multiSearchUsersCount / histories.size()) * 100D
        );
    }

    private static Collection<UserHistory> convertToHistories(List<Log> logs) {
        Map<String, UserHistory> histories = new HashMap<>();

        for (Log log : logs) {
            UserHistory history = histories.computeIfAbsent(log.uuid(), UserHistory::new);
            history.actions().add(log.action());
        }

        return histories.values();
    }

    private static List<Log> loadLogs() throws Exception {
        Path filePath = Paths.get("mobile_app_log_202406061523.csv");
        try (Stream<String> lines = Files.lines(filePath, StandardCharsets.UTF_8)) {
            return lines.skip(1L)
                    .map(Log::parse)
                    .sorted(Comparator.comparingLong(Log::time))
                    .toList();
        }
    }
}