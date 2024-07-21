package com.derits.multiselect;

import java.util.ArrayList;
import java.util.List;

public record UserHistory(
        String uuid,
        List<Action> actions
) {

    public UserHistory(String uuid) {
        this(uuid, new ArrayList<>());
    }

    public boolean hasMultiSearch() {
        if (actions.size() >= 3) {
            int countOfSelects = 0;
            for (Action action : actions) {
                if (action == Action.UNKNOWN)
                    continue;

                if (action == Action.SELECT) {
                    countOfSelects++;
                    continue;
                }

                // action: show_ads
                if (countOfSelects > 1)
                    return true;

                countOfSelects = 0;
            }
        }

        return false;
    }

}