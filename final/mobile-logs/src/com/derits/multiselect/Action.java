package com.derits.multiselect;


public enum Action {
    UNKNOWN,
    SELECT,
    SHOW_ADS,
    ;

    public static Action parse(String value) {
        return switch (value.toLowerCase()) {
            case "модель выбрана", "марка выбрана" -> SELECT;
            case "показать объявления" -> SHOW_ADS;
            default -> UNKNOWN;
        };
    }
}
