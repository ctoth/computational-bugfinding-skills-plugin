# Search a missing access interaction

These are this pack's experiment-design choices, not promised bug yield. Their basis is the historical study's publication, initialization and reference-count examples and warning about excess synchronization ([TSan 2009, §§6.3–7.1, pp.67–69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)); runtime selection follows the current references.

## Construct a meaningful lifecycle

Name the real producer, live object, competing access contexts and expected synchronization. Generate valid public operations establishing create → publish → concurrent use → replace/cancel/close. Preserve actual returned identities and required setup. Do not replace a target-owned lifecycle with an idealized mock or count invalid-handle setup failures as this interaction.

Record which operations completed and whether the relevant access paths actually occurred. Source coverage is useful reach evidence, but does not itself establish that two contexts shared the same live object. The original study's object-publication ("One thread initializes an object pointer") and reference-count cases required that relationship ([TSan 2009, §§6.3.4, 6.4.3 and 7.1, pp.67–69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

A test barrier can establish a launch phase; wrapping each entire target operation in one test mutex can remove the competition. Preserve genuine synchronization semantics rather than adding observer annotations to make a warning disappear ([TSan 2009, §5 and §6.5, pp.65–66,69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

## Worked pilot

Illustrative, unexecuted: an existing service test creates a handle, runs readers, then reloads or closes it. Existing load tests never close handles. Use the real supported lifecycle and a bounded small actor set; retain identity and raw access reports. Vary the use/close overlap and state-establishing prefix. If the relevant path remains absent, fix the existing harness owner when authorized before multiplying workers.

Classify an expected closed-handle error separately from a conflicting-access report. A report can precede a much later allocator symptom (in Chromium, "one of the subsequent calls to `malloc` failed"); do not require a crash before retaining the access evidence ([TSan 2009, §7.1, p.69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

Use `stateful-property-testing` for admissible sequences, `harness-sensitivity` for representative controls, and `schedule-exploration` when the target has a supported controllable scheduler.
