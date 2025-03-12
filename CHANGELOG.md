# Changelog

## v1.3.2 (2025-02-26 23:00:09 -0300)

- f9d1660 added pytest.ini (to config pytest) added utils.SocketServer and SocketClient
- 1a169fe added utils.FileHandler; Fixed minor bugs in ThreadBase; Added syntatic sugar to method Publisher.subcribe()
- da77837 improved docs to Sphinx docstring format; fixed Publisher implementation (from SafeSet to SafeList)
- f668eb3 bug fix
- 104cf20 release version v1.3.1

## v1.3.1 (2025-02-20 17:57:46 -0300)

- 104cf20 release version v1.3.1
- 9688c75 bug fix
- f14c7f3 improved docs, added img/ for docs/, added SVG images for docs
- b8e39c4 fix docs
- a3b6c55 fix docs
- 270cb73 release version v1.3.0

## v1.3.0 (2025-02-20 16:42:53 -0300)

- 270cb73 release version v1.3.0
- 1e358aa added utils.Publish and utils.Subscribe fixed circular import in datatype.__init__ => datatype.SafeObjBase => utils.Factory => utils.__init__ => utils.Publisher => datatype.SafeSet => datatype.__init__
- 0403868 added stop_join() to facilitate library usage (*syntatic sugar*)
- adb5669 added multithread capabilities to PipelineStage moved thread.PipelineStage and Pipeline to utils package (they use ThreadBase, but they are not a subclass of it)
- a31226c release version v1.2.0

## v1.2.0 (2025-02-19 17:38:26 -0300)

- a31226c release version v1.2.0
- 6a177b9 added utils.Pipeline to automate multi-stage pipeline creation, based on thread.PipelineStage
- 1daea17 changed thread.Pipeline => thread.PipelineStage added Raises RuntimeError docstring for ThreadBase.join
- a23cd8d major bug fixes; avoid name collisions (using name mangling); modified ThreadBase to allow repeated execution and added stop() method; added run_examples.bat (test all examples/**/*.py files)
- fb73c16 big fix in docs
- 80c502a improved docs
- 5afc4eb release version v1.1.0

## v1.1.0 (2025-02-18 12:01:33 -0300)

- 5afc4eb release version v1.1.0
- ce265b6 added ThreadBase.CallableException added thread.Scheduler class
- f3b5bb5 improved exception mgmnt in Subprocess
- 0330fc6 improved Pipeline Exception handling
- 6b31f5d fixed some Pipeline tests
- a730fed added thread.Pipeline class

## v1.0.2 (2025-02-17 18:05:23 -0300)

- a730fed added thread.Pipeline class
- 9985cbf added ThreadBase in safethread.thread

## v1.0.1 (2025-02-17 01:29:26 -0300)

- 9985cbf added ThreadBase in safethread.thread
- 205481a improved docs
- 214d047 added utils.Subprocess added examples/ folder fixed min req. Python version >= 3.11 improved docs/ and .md files

## v1.0.0 (2025-02-17 00:41:24 -0300)

- 214d047 added utils.Subprocess added examples/ folder fixed min req. Python version >= 3.11 improved docs/ and .md files
- 1ffef56 added SafeQueue improved data initialization method __init__() fixed already thread safe data structures inheritance (using Python MRO)

## v0.2.0 (2025-02-16 22:09:46 -0300)

- 1ffef56 added SafeQueue improved data initialization method __init__() fixed already thread safe data structures inheritance (using Python MRO)
- 270e55e release version v0.1.1

## v0.1.1 (2025-02-16 21:13:03 -0300)

- 270e55e release version v0.1.1
- ccff69e bug fix
- 32e8b35 improved docs and .md files
- 332dd1c improved .md github docs
- 723d4db added classifiers
- 41695ac bug fix
- 5d8402c release version v0.1.0

## v0.1.0 (2025-02-16 19:30:59 -0300)

- 5d8402c release version v0.1.0
- 51d14d7 fixed CHANGELOG generate script to include all commits in between tags (versions) fixed docs to include package docstring added SafeList and SafeDict datatypes
- 10d7f5f fix bug
- ac0d7c9 added index.html
- c99ad22 removed markdown docs and added docs link
- 1ecf83b added markdown documentation in docs/
- ee48be4 bug fix
- 56fa2e8 release version v0.0.4

## v0.0.4 (2025-02-14 15:50:01 -0300)

- 56fa2e8 release version v0.0.4
- e9f6c1f bug fix
- 0118ff9 bug fix
- 95f8efe added docs/ folder added pdocs and pytest added Factory and Singleton classes and tests
- 6574710 release version 0.0.3

## v0.0.3 (2025-02-14 12:24:16 -0300)

- 6574710 release version 0.0.3
- a88bc5f release version 0.0.2

## v0.0.2 (2025-02-14 12:01:09 -0300)

- a88bc5f release version 0.0.2
- 633bc5b added utilitary scripts to build and publish package

## v0.0.1 (2025-02-13 18:11:57 -0300)

- 633bc5b added utilitary scripts to build and publish package

