CMPU UNIPOLAR COMPATIBILITY PATCH v2   -   v1.3.0
Cheat Menu Pro (3717461054) + UNIPOLAR (pdx_118232)
================================================================

INSTALLATION
----------------------------------------------------------------
1. Close Victoria 3 completely.
2. Extract the zip into ...\Documents\Paradox Interactive\Victoria 3\mod\
   (choose "Replace" for the files).
3. Enable BOTH mods, the patch AFTER Cheat Menu Pro:
      - Cheat Menu Pro                                  (3717461054)
      - Cheat Menu Pro - UNIPOLAR Compatibility Patch2
4. Start a game. Open the cheat menu -> "State and Building".

WHAT THIS PATCH DOES (v1.0 - v1.3)
================================================================

1) "LEVELS" BUTTON  (State and Building -> Building tab)
----------------------------------------------------------------
A green button labelled "Levels: N" now sits between the "Building" and
"Building Adjust" tabs. It shows how many levels the building that is
currently selected in the building picker already has in the states that
are marked for the cheat mechanics. Read-only, updates live.

2) THE OVERFLOWING FEEDBACK LIST IS GONE
----------------------------------------------------------------
The old feedback drawer was permanently visible and listed every building
at once, which flooded the screen. It is now hidden by default and, when
opened with the "Levels" button, shows only the currently selected
building plus a Close button.

3) "SELECTED BUILDING" INDICATOR FIXED
----------------------------------------------------------------
The indicator never appeared for the 24 UNIPOLAR special buildings (they
were checked against the wrong key, e.g. "airport" instead of
"building_airport"). It works now. It was also moved down 5 px so the
new Levels button does not overlap it.

4) INTEREST GROUPS AND IDEOLOGIES REBUILT FOR UNIPOLAR
----------------------------------------------------------------
THIS IS THE "SOME THINGS WORK, SOME DON'T" PROBLEM.

UNIPOLAR replaces common/ideologies/00_ig_ideologies.txt and replaces the
vanilla interest group definitions with its own versions:

  * 26 vanilla ideologies were DELETED (liberal, reactionary, jingoist,
    loyalist, patriotic, moralist, pious, socialist, ...).
    55 of the 77 ideology buttons of the cheat menu pointed at those
    deleted ideologies, so clicking them did NOTHING (silent no-op).
  * UNIPOLAR has its own 21 ideologies (Right/Left/Far Left Economy,
    Globalist, Nationalist, Regionalist, Totalitarian, Authoritarian,
    Communitarian, Traditionalist, Conservative, Progressive, Monarchist,
    Republican, Theocrat, Militarist, Communist, ...) and its own
    interest group list, which also includes a 9th group:
    "Professionals" (ig_professionals).

What this patch does:
  * The ideology grid now shows the 46 ideologies that really exist in
    UNIPOLAR, with their real names, their real icons and a tooltip that
    lists the interest groups supporting each of them.
    Left click adds the ideology to the selected interest group,
    right click removes it.
  * "Professionals" was added to the interest group selector row, and the
    approval / political strength / pop attraction buttons now work on it
    as well.
  * The vanilla 8 interest groups keep working exactly as before
    (their modifier types still exist in the game).

5) POPULATION GENERATOR - CONFIRMATION POPUP
----------------------------------------------------------------
The Population tab of the State and Building panel was confusing. Now
every "Start" button opens a confirmation window that spells out what is
going to happen before anything is executed:

  * how many pops will be ADDED
  * the workforce ratio (how many of them are working adults)
  * the literacy of the new pops
  * which culture they will get
  * where they will appear:
      - "Spawn at Home"      -> ONE of your marked states (picked at random)
      - "Spawn in Target"    -> ONE of the marked country's marked states
      - alt-click on "Start" -> ALL of your homeland states
  * and the important bit: the pops are created INSTANTLY (same tick),
    they are ADDED to the target state and existing population is never
    removed - a smaller number than the current population does not
    subtract anything.

ROLLBACK
----------------------------------------------------------------
Backups of the replaced files are in the _dev_scripts folder:
   gui_main_sakuya_main.gui.pre_levels_backup
   gui_main_sakuya_main.gui.pre_unipolar_ig_backup
   gui_main_sakuya_main.gui.pre_popgen_backup
   loc_cmpu_feedback_l_english.yml.pre_levels_backup
Copy them back over the patched files to undo everything.

FOLDER CONTENTS
----------------------------------------------------------------
.metadata/           mod metadata
common/              scripted guis, script values, static modifiers
gui/                 the Cheat Menu Pro interface (patched copy)
localization/english/ English strings of the patch
_dev_scripts/        development leftovers (python scripts, old zips,
                      backups). The game ignores this folder, it is only
                      there so the mod folder is not full of junk.
