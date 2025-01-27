#!/usr/bin/env python3

HEADER= '''
<script defer data-domain="nondocumentation.garambrogne.net" src="https://plausible.garambrogne.net/js/script.js"></script>

<script src="https://cdn.jsdelivr.net/npm/jquery"></script>
<script src="https://cdn.jsdelivr.net/npm/jquery.terminal@2.35.2/js/jquery.terminal.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jquery.terminal@2.35.2/js/unix_formatting.min.js"></script>

<link
    href="https://cdn.jsdelivr.net/npm/jquery.terminal@2.35.2/css/jquery.terminal.min.css"
    rel="stylesheet"
/>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
'''

CSS='''
html, body {
  font-family: "Open Sans", serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
  font-variation-settings:
    "wdth" 100;
}

code {
  font-family: "Fira Code", serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
}

            .terminal {
                --size: 1.1;
                --color: rgba(255, 255, 255, 0.8);
                /*width: 640px;
                height: 480px;
                border: thin dotted red;*/
                overflow: scroll;
            }

            .noblink {
                --animation: terminal-none;
            }
            #console,
            #screen {
                display: block;
                width: 480px;
                height: 180px;
            }
            #console {
                /*display: none;*/
                background-color: black;
                margin-left: 50px;
                border: 4px solid lightgrey;
                z-order: 99;
                color: lightgrey;
            }
            #python-repl {
                position: fixed;
                bottom: 0;
                right: -480px;
                z-index: 100;
                transition: right 1s;
            }

            /* https://cssloaders.github.io/ */
            .loader {
                margin-top: -100px;
                margin-left: 220px;
                width: 16px;
                height: 16px;
                border-radius: 50%;
                background-color: #fff;
                box-shadow:
                    32px 0 #fff,
                    -32px 0 #fff;
                position: relative;
                animation: flash 0.5s ease-out infinite alternate;
            }

            @keyframes flash {
                0% {
                    background-color: #fff2;
                    box-shadow:
                        32px 0 #fff2,
                        -32px 0 #fff;
                }
                50% {
                    background-color: #fff;
                    box-shadow:
                        32px 0 #fff2,
                        -32px 0 #fff2;
                }
                100% {
                    background-color: #fff2;
                    box-shadow:
                        32px 0 #fff,
                        -32px 0 #fff2;
                }
            }

            #screen {
                padding: 5px;
                font-weight: bolder;
                transition: opacity 5s;
            }
            button.term {
                float: left;
                background-color: black;
                border-radius: 10px 0 0 10px;
                border: 4px solid lightgrey;
                color: lightgrey;
                width: 54px;
                text-align: center;
                font-size: 14px;
                font-weight: bolder;
                padding-bottom: 7px;
                border-right: none;
                z-index: 100;
                /*padding: 0px 10px 7px 10px;*/
            }
            button.term:hover {
                background-color: darkgrey;
            }
'''

BODY = '''
        <div id="python-repl">
            <button class="term">>_</button>
            <div id="console">
                <div id="screen"></div>
                <div class="loader"></div>
            </div>
        </div>
'''

FOOTER = '''
        <script>
            "use strict";

            var toggle = true;
            var started = false;
            const button = $("button.term");
            const s = $("#console");
            const repl = $("#python-repl");
            button.click(() => {
                button.toggleClass("on");
                if (toggle) {
                    button.html("X");
                    /*repl.css('animation', 'slide-left 1s linear');*/
                    repl.css("right", "0");
                    if (!started) {
                        console.log("start");
                        window.console_ready = initWorker();
                    }
                } else {
                    button.html(">_");
                    /*repl.css('animation', 'slide-right 0.5s linear');*/
                    repl.css('right', '-480px');
                }
                toggle = !toggle;
            });

            function sleep(s) {
                return new Promise((resolve) => setTimeout(resolve, s));
            }
            function initWorker() {
                var resultPromiseResolver;
                var completedPromiseResolver;
                var clearPromiseResolver;
                globalThis.pyodide_worker = new Worker("console_webworker.js", {
                    type: "module",
                });
                pyodide_worker.onmessage = async function (e) {
                    const data = e.data;
                    if (data.type === "init") {
                        main(data["banner"]);
                    } else if (data.type === "echo") {
                        term.echo(
                            data["msg"]
                                .replaceAll("]]", "&rsqb;&rsqb;")
                                .replaceAll("[[", "&lsqb;&lsqb;"),
                            ...data["opts"],
                        );
                    } else if (data.type === "error") {
                        term.error(data["str"]);
                    } else if (data.type === "result") {
                        if (resultPromiseResolver) {
                            resultPromiseResolver(data);
                        } else {
                            console.log("Result message while not waiting?");
                        }
                    } else if (data.type === "clear") {
                        if (clearPromiseResolver) {
                            clearPromiseResolver(data);
                        } else {
                            console.log("Cleared message while not waiting?");
                        }
                    } else if (data.type === "complete") {
                        if (completedPromiseResolver) {
                            completedPromiseResolver(data.result);
                        } else {
                            console.log(
                                "Completion message while not waiting?",
                            );
                        }
                    } else if (data.type === "fatal") {
                        if (e.name === "Exit") {
                            term.error(e);
                            term.error(
                                "Pyodide exited and can no longer be used.",
                            );
                        } else {
                            term.error(
                                "Pyodide has suffered a fatal error. Please report this to the Pyodide maintainers.",
                            );
                            term.error("The cause of the fatal error was:");
                            term.error(e);
                            term.error(
                                "Look in the browser console for more details.",
                            );
                        }
                    }
                };
                globalThis.do_push = async function (str) {
                    let promise = new Promise((resolve, reject) => {
                        resultPromiseResolver = resolve;
                    });
                    pyodide_worker.postMessage({ type: "push", value: str });
                    let retval = await promise;
                    resultPromiseResolver = undefined;
                    return await promise;
                };
                globalThis.do_complete = async function (str) {
                    let promise = new Promise((resolve, reject) => {
                        completedPromiseResolver = resolve;
                    });
                    pyodide_worker.postMessage({
                        type: "complete",
                        value: str,
                    });
                    let retval = await promise;
                    completedPromiseResolver = undefined;
                    return retval;
                };
                globalThis.do_clear = async function () {
                    let promise = new Promise((resolve, reject) => {
                        clearPromiseResolver = resolve;
                    });
                    pyodide_worker.postMessage({ type: "clear", value: str });
                    let retval = await promise;
                    clearPromiseResolver = undefined;
                    return await promise;
                };
            }
            async function main(pyodide_version_banner) {
                const ps1 = ">>> ";
                const ps2 = "... ";

                async function lock() {
                    let resolve;
                    const ready = term.ready;
                    term.ready = new Promise((res) => (resolve = res));
                    await ready;
                    return resolve;
                }

                async function interpreter(command) {
                    const unlock = await lock();
                    term.pause();
                    // multiline should be split (useful when pasting)
                    for (const c of command.split("\\n")) {
                        const escaped = c.replaceAll(/\\u00a0/g, " ");
                        const fut = await do_push(escaped);
                        term.set_prompt(
                            fut.syntax_check === "incomplete" ? ps2 : ps1,
                        );
                        switch (fut.syntax_check) {
                            case "syntax-error":
                                term.error(fut.formatted_error.trimEnd());
                                continue;
                            case "incomplete":
                                continue;
                            case "complete":
                                break;
                            default:
                                throw new Error(`Unexpected type ${ty}`);
                        }
                    }
                    term.resume();
                    await sleep(10);
                    unlock();
                }

                globalThis.term = $("#screen").terminal(interpreter, {
                    greetings: pyodide_version_banner,
                    prompt: ps1,
                    completionEscape: false,
                    completion: function (command, callback) {
                        do_complete(command).then((result) => callback(result));
                    },
                    keymap: {
                        "CTRL+C": async function (event, original) {
                            await do_clear();
                            term.enter();
                            echo("KeyboardInterrupt");
                            term.set_command("");
                            term.set_prompt(ps1);
                        },
                        TAB: (event, original) => {
                            const command = term.before_cursor();
                            // Disable completion for whitespaces.
                            if (command.trim() === "") {
                                term.insert("\\t");
                                return false;
                            }
                            return original(event);
                        },
                    },
                    onInit: () => {
                        console.log("init");
                        $(".loader").css("display", "none");
                    },
                });
                globalThis.term.resize(480, 180);
                window.term = term;
                term.ready = Promise.resolve();

                const searchParams = new URLSearchParams(
                    window.location.search,
                );
                if (searchParams.has("noblink")) {
                    $(".cmd-cursor").addClass("noblink");
                }

                let idbkvPromise;
                async function getIDBKV() {
                    if (!idbkvPromise) {
                        idbkvPromise = await import(
                            "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js"
                        );
                    }
                    return idbkvPromise;
                }

                async function mountDirectory(pyodideDirectory, directoryKey) {
                    if (pyodide.FS.analyzePath(pyodideDirectory).exists) {
                        return;
                    }
                    const { get, set } = await getIDBKV();
                    const opts = {
                        id: "mountdirid",
                        mode: "readwrite",
                    };
                    let directoryHandle = await get(directoryKey);
                    if (!directoryHandle) {
                        directoryHandle = await showDirectoryPicker(opts);
                        await set(directoryKey, directoryHandle);
                    }
                    const permissionStatus =
                        await directoryHandle.requestPermission(opts);
                    if (permissionStatus !== "granted") {
                        throw new Error(
                            "readwrite access to directory not granted",
                        );
                    }
                    await pyodide.mountNativeFS(
                        pyodideDirectory,
                        directoryHandle,
                    );
                }
                globalThis.mountDirectory = mountDirectory;
            }
        </script>
'''

def patch(src, target):
    for line in src.readlines():
        if line.strip()=='</style>':
            target.write(CSS)
            target.write(line)
        elif line.strip().startswith("<head"):
            target.write(line)
            target.write(HEADER)
        elif line.strip().startswith("<body"):
            target.write(line)
            target.write(BODY)
        elif line.strip().startswith("</body"):
            target.write(FOOTER)
            target.write(line)
        else:
            target.write(line)


if __name__ == "__main__":
    patch(open('output/index.html', 'r'), open('output/index_patched.html','w'))
