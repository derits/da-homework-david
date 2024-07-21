package com.derits.multiselect;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;

public record Log(
        long time,
        Action action,
        String uuid
) {

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public static Log parse(String line) {
        String[] parts = line.split(";");

        String rawTime = parts[2];

        // Для использования "tme", вместо "clientTime"
//            String rawTime = parts[1];
//            int dotIndex = rawTime.indexOf(".");
//            if (dotIndex != -1)
//                rawTime = rawTime.substring(0, dotIndex);


        LocalDateTime dateTime = DATE_TIME_FORMATTER.parse(rawTime, LocalDateTime::from);
        long time = dateTime.toInstant(ZoneOffset.UTC).toEpochMilli();

        String rawAction = parts[4];
        Action action = Action.parse(rawAction);

//         если брать выборы только "из списка"
//        if (action == Action.SELECT && !"из топа".equalsIgnoreCase(parts[5]))
//            action = Action.UNKNOWN;

        String rawUuid = parts[6].trim();
        String uuid = rawUuid.replace("\"", "");

        return new Log(time, action, uuid);
    }

}