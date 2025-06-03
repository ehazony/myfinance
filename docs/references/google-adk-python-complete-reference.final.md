================================================
================================================
# Agent Development Kit (ADK)
[![r/agentdevelopmentkit](https://img.shields.io/badge/Reddit-r%2Fagentdevelopmentkit-FF4500?style=flat&logo=reddit&logoColor=white)](https://www.reddit.com/r/agentdevelopmentkit/)
<html>
    <h2 align="center">
    </h2>
    <h3 align="center">
      An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control.
    </h3>
    <h3 align="center">
      Important Links:
    </h3>
</html>
---
## ✨ Key Features
- **Rich Tool Ecosystem**: Utilize pre-built tools, custom functions,
  OpenAPI specs, or integrate existing tools to give agents diverse
  capabilities, all for tight integration with the Google ecosystem.
- **Code-First Development**: Define agent logic, tools, and orchestration
- **Modular Multi-Agent Systems**: Design scalable applications by composing
  multiple specialized agents into flexible hierarchies.
- **Deploy Anywhere**: Easily containerize and deploy agents on Cloud Run or
  scale seamlessly with Vertex AI Agent Engine.
## 🤖 Agent2Agent (A2A) Protocol and ADK Integration
For remote agent-to-agent communication, ADK integrates with the
for how they can work together.
## 🚀 Installation
### Stable Release (Recommended)
```bash
pip install google-adk
```
The release cadence is weekly.
This version is recommended for most users as it represents the most recent official release.
### Development Version
Bug fixes and new features are merged into the main branch on GitHub first. If you need access to changes that haven't been included in an official PyPI release yet, you can install directly from the main branch:
```bash
```
## 📚 Documentation
Explore the full documentation for detailed guides on building, evaluating, and
deploying agents:
## 🏁 Feature Highlight
### Define a single agent:
```python
from google.adk.agents import Agent
from google.adk.tools import google_search
root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash", # Or your preferred Gemini model
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```
### Define a multi-agent system:
Define a multi-agent system with coordinator agent, greeter agent, and task execution agent. Then ADK engine and the model will guide the agents works together to accomplish the task.
```python
from google.adk.agents import LlmAgent, BaseAgent
# Define individual agents
greeter = LlmAgent(name="greeter", model="gemini-2.0-flash", ...)
task_executor = LlmAgent(name="task_executor", model="gemini-2.0-flash", ...)
# Create parent agent and assign children via sub_agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[ # Assign sub_agents here
        greeter,
        task_executor
    ]
)
```
### Development UI
###  Evaluate Agents
```bash
adk eval \
```
## 🤝 Contributing
## 📄 License
---
*Happy Agent Building!*
================================================
================================================
## 1.1.1
### Features
## 1.1.0
### Features
* Extract agent loading logic from fast_api.py to a separate AgentLoader class and support more agent definition folder/file structure.
* Added audio play in web UI.
* Added input transcription support for live/streaming.
* Added support for storing eval run history locally in adk eval cli.
* Image artifacts can now be clicked directly in chat message to view.
* Left side panel can now be resized.
### Bug Fixes
* Avoid duplicating log in stderr.
* Align event filtering and ordering logic.
* Add handling for None param.annotation.
* Fixed several minor bugs regarding eval tab in web UI.
### Miscellaneous Chores
* Add google search agent in samples.
* Update filtered schema parameters for Gemini API.
* Adds autoformat.sh for formatting codebase.
## 1.0.0
### ⚠ BREAKING CHANGES
* Evaluation dataset schema is finalized with strong-type pydantic models.
  (previously saved eval file needs re-generation, for both adk eval cli and
  the eval tab in adk web UI).
* `BuiltInCodeExecutor` (in code_executors package) replaces
  `BuiltInCodeExecutionTool` (previously in tools package).
* All methods in services are now async, including session service, artifact
  service and memory service.
  * `list_events` and `close_session` methods are removed from session service.
  Old format is not working anymore.
* `Memory` schema and `MemoryService` is redesigned.
* Mark various class attributes as private in the classes in the `tools` package.
* Disabled session state injection if instruction provider is used.
  (so that you can have `{var_name}` in the instruction, which is required for code snippets)
* Toolbox integration is revamped: tools/toolbox_tool.py → tools/toolbox_toolset.py.
* Removes the experimental `remote_agent.py`. We'll redesign it and bring it back.
### Features
* Dev UI:
  * A brand new trace view for overall agent invocation.
  * A revamped evaluation tab and comparison view for checking eval results.
* Introduced `BaseToolset` to allow dynamically add/remove tools for agents.
  * Revamped MCPToolset with the new BaseToolset interface.
  * Revamped GoogleApiTool, GoogleApiToolset and ApplicationIntegrationToolset with the new BaseToolset interface.
  * Resigned agent.py file structure when needing MCPToolset.
  * Added ToolboxToolset.
* Redesigned strong-typed agent evaluation schema.
  * Allows users to create more cohesive eval sets.
  * Allows evals to be extended for non-text modality.
  * Allows for a structured interaction with the uber eval system.
* Redesigned Memory schema and MemoryService interfaces.
* Added token usage to LlmResponse.
* Allowed specifying `--adk_version` in `adk deploy cloud_run` cli. Default is the current version.
### Bug Fixes
* Fixed `adk deploy cloud_run` failing bug.
* Fixed logs not being printed due to `google-auth` library.
### Miscellaneous Chores
* Display full help text when adk cli receives invalid arguments.
* `adk web` now binds `127.0.0.1` by default, instead of 0.0.0.0.
* `InMemoryRunner` now takes `BaseAgent` in constructor.
* Various docstring improvements.
* Various UI tweaks.
* Various bug fixes.
## 0.5.0
### ⚠ BREAKING CHANGES
* Updated artifact and memory service interface to be async. Agents that
  interact with these services through callbacks or tools will now need to
  adjust their invocation methods to be async (using await), or ensure calls
  are wrapped in an asynchronous executor like asyncio.run(). Any service that
  extends the base interface must also be updated.
### Features
* Introduced the ability to chain model callbacks.
* Added support for async agent and model callbacks.
* Added input transcription support for live/streaming.
* Captured all agent code error and display on UI.
* Set param required tag to False by default in openapi_tool.
* Updated evaluation functions to be asynchronous.
### Bug Fixes
* Ensured a unique ID is generated for every event.
* Fixed the issue when openapi_specparser has parameter.required as None.
* Updated the 'type' value on the items/properties nested structures for Anthropic models to adhere to JSON schema.
* Fix litellm error issues.
### Miscellaneous Chores
* Regenerated API docs.
* Created a `developer` folder and added samples.
* Docstring improvements, typo fixings, GitHub action to enforce code styles on formatting and imports, etc.
## 0.4.0
### ⚠ BREAKING CHANGES
* Set the max size of strings in database columns. MySQL mandates that all VARCHAR-type fields must specify their lengths.
* Extract content encode/decode logic to a shared util, resolve issues with JSON serialization, and update key length for DB table to avoid key too long issue in mysql.
* Enhance `FunctionTool` to verify if the model is providing all the mandatory arguments.
### Features
* Update ADK setup guide to improve onboarding experience.
* feat: add ordering to recent events in database session service.
* feat(llm_flows): support async before/after tool callbacks.
* feat: Added --replay and --resume options to adk run cli. Check adk run --help for more details.
* Created a new Integration Connector Tool (underlying of the ApplicationIntegrationToolSet) so that we do not force LLM to provide default value.
### Bug Fixes
* Don't send content with empty text to LLM.
* Fix google search reading undefined for `renderedContent`.
### Miscellaneous Chores
## 0.3.0
### ⚠ BREAKING CHANGES
* Auth: expose `access_token` and `refresh_token` at top level of auth
  credentials, instead of a `dict`
### Features
* Added support for running agents with MCPToolset easily on `adk web`.
* Added `custom_metadata` field to `LlmResponse`, which can be used to tag
  LlmResponse via `after_model_callback`.
* Added `--session_db_url` to `adk deploy cloud_run` option.
* Many Dev UI improvements:
  * Better google search result rendering.
  * Show websocket close reason in Dev UI.
  * Better error message showing for audio/video.
### Bug Fixes
* Fixed MCP tool json schema parsing issue.
* Fixed issues in DatabaseSessionService that leads to crash.
* Fixed functions.py.
* Fixed `skip_summarization` behavior in `AgentTool`.
### Miscellaneous Chores
* Various code improvements.
* Various typo fixes.
* Bump min version of google-genai to 1.11.0.
## 0.2.0
### ⚠ BREAKING CHANGES
* Fix typo in method name in `Event`: has_trailing_code_exeuction_result --> has_trailing_code_execution_result.
### Features
* `adk` CLI:
  * Introduce `adk create` cli tool to help creating agents.
  * Adds `--verbosity` option to `adk deploy cloud_run` to show detailed cloud
    run deploy logging.
* Improve the initialization error message for `DatabaseSessionService`.
* Lazy loading for Google 1P tools to minimize the initial latency.
* Support emitting state-change-only events from planners.
* Lots of Dev UI updates, including:
  * Show planner thoughts and actions in the Dev UI.
  * Support MCP tools in Dev UI.
    (NOTE: `agent.py` interface is temp solution and is subject to change)
  * Auto-select the only app if only one app is available.
  * Show grounding links generated by Google Search Tool.
* `.env` file is reloaded on every agent run.
### Bug Fixes
* `LiteLlm`: arg parsing error and python 3.9 compatibility.
* `DatabaseSessionService`: adds the missing fields; fixes event with empty
  content not being persisted.
* Google API Discovery response parsing issue.
* `load_memory_tool` rendering issue in Dev UI.
* Markdown text overflows in Dev UI.
### Miscellaneous Chores
* Various typo fixes.
## 0.1.0
### Features
* Initial release of the Agent Development Kit (ADK).
* Tool authentication support
* Rich tool support, e.g. built-in tools, google-cloud tools, third-party tools, and MCP tools
* Rich callback support
* Built-in code execution capability
* Asynchronous runtime and execution
* Session, and memory support
* Built-in evaluation support
* Development UI that makes local development easy
* Deploy to Google Cloud Run, Agent Engine
* (Experimental) Live(Bidi) audio/video agent support and Compositional Function Calling(CFC) support
================================================
================================================
- [Before you begin](#before-you-begin)
  - [Review our community guidelines](#review-our-community-guidelines)
  - [Finding Issues to Work On](#finding-issues-to-work-on)
  - [Large or Complex Changes](#large-or-complex-changes)
  - [Documentation](#documentation)
  - [Development Setup](#development-setup)
  - [Code reviews](#code-reviews)
# Before you begin
## Sign our Contributor License Agreement
Contributions to this project must be accompanied by a
[Contributor License Agreement](https://cla.developers.google.com/about) (CLA).
project.
If you or your current employer have already signed the Google CLA (even if it
was for a different project), you probably don't need to do it again.
Visit <https://cla.developers.google.com/> to see your current agreements or to
sign a new one.
## Review our community guidelines
This project follows
[Google's Open Source Community Guidelines](https://opensource.google/conduct/).
## Finding Issues to Work On
- For bug fixes or features, please provide logs or screenshot after the fix is applied to help reviewers better understand the fix.
## Large or Complex Changes
For substantial features or architectural revisions:
- Open an Issue First: Outline your proposal, including design considerations and impact.
- Gather Feedback: Discuss with maintainers and the community to ensure alignment and avoid duplicate work
- **Coverage:** Cover new features, edge cases, error conditions, and typical use cases.
  - Fast and isolated.
  - Written clearly with descriptive names.
  - Free of external dependencies (use mocks or fixtures as needed).
- **Quality:** Aim for high readability and maintainability; include docstrings or comments for complex scenarios.
Depending on your change:
- **ADK Web:**
  - Use the `adk web` to verify functionality.
  - Capture and attach relevant screenshots demonstrating the UI/UX changes or outputs.
- **Runner:**
  - Highlight sections of the log that directly relate to your change.
## Documentation
## Development Setup
1.  **Clone the repository:**
    ```shell
    gh repo clone google/adk-python
    cd adk-python
    ```
2.  **Install uv:**
    Check out [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).
3.  **Create and activate a virtual environment:**
    **NOTE**: ADK supports Python 3.9+. Python 3.11 and above is strongly recommended.
    Create a workspace venv using uv.
    ```shell
    uv venv --python "python3.11" ".venv"
    ```
    Activate the workspace venv.
    ```shell
    source .venv/bin/activate
    ```
    **windows**
    ```shell
    source .\.venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```shell
    uv sync --all-extras
    ```
    **NOTE**: for convenience, installing all extra deps as a starting point.
    ```shell
    ```
    extra dependencies.
    ```shell
    ```
6.  **Auto-format the code:**
    **NOTE**: We use `isort` and `pyink` for styles. Use the included
    autoformat.sh to auto-format.
    ```shell
    ./autoformat.sh
    ```
7. **Build the wheel file:**
    ```shell
    uv build
    ```
    Create a clean venv and activate it:
    ```shell
    VENV_PATH=~/venvs/adk-quickstart
    ```
    ```shell
    command -v deactivate >/dev/null 2>&1 && deactivate
    ```
    ```shell
    rm -rf $VENV_PATH \
      && python3 -m venv $VENV_PATH \
      && source $VENV_PATH/bin/activate
    ```
    Install the locally built wheel file:
    ```shell
    pip install dist/google_adk-<version>-py3-none-any.whl
    ```
## Contributing Resources
## Code reviews
All submissions, including submissions by project members, require review. We
================================================
================================================
                                 Apache License
                           Version 2.0, January 2004
   1. Definitions.
      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.
      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.
      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.
      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.
      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.
      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.
      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).
      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.
      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."
      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      Work and such Derivative Works in Source or Object form.
   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      use, offer to sell, sell, import, and otherwise transfer the Work,
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.
   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:
      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and
      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and
      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and
      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.
      You may add Your own copyright statement to Your modifications and
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.
   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      with Licensor regarding such Contributions.
   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.
   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.
   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.
   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.
   END OF TERMS AND CONDITIONS
   APPENDIX: How to apply the Apache License to your work.
      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
================================================
File: autoformat.sh
================================================
#!/bin/bash
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# Autoformat ADK codebase.
if ! command -v isort &> /dev/null
then
    exit
fi
if ! command -v pyink &> /dev/null
then
    exit
fi
echo '---------------------------------------'
echo '|  Organizing imports for src/...'
echo '---------------------------------------'
isort src/
echo 'All done! ✨ 🍰 ✨'
echo '---------------------------------------'
echo '---------------------------------------'
echo 'All done! ✨ 🍰 ✨'
echo '---------------------------------------'
echo '|  Auto-formatting src/...'
echo '---------------------------------------'
echo '---------------------------------------'
echo '---------------------------------------'
================================================
File: pylintrc
================================================
# This Pylint rcfile contains a best-effort configuration to uphold the
# best-practices and style described in the Google Python style guide:
#
# Its canonical open-source location is:
[MAIN]
# Files or directories to be skipped. They should be base names, not paths.
ignore=third_party
# Files or directories matching the regex patterns are skipped. The regex
# matches against base names, not paths.
ignore-patterns=
# Pickle collected data for later comparisons.
persistent=no
# List of plugins (as comma separated values of python modules names) to load,
# usually to register additional checkers.
load-plugins=
# Use multiple processes to speed up Pylint.
jobs=4
# Allow loading of arbitrary C extensions. Extensions are imported into the
# active Python interpreter and may run arbitrary code.
unsafe-load-any-extension=no
[MESSAGES CONTROL]
# Only show warnings with the listed confidence levels. Leave empty to show
# all. Valid levels: HIGH, INFERENCE, INFERENCE_FAILURE, UNDEFINED
confidence=
# Enable the message, report, category or checker with the given id(s). You can
# either give multiple identifier separated by comma (,) or put this option
# multiple time (only on the command line, not in the configuration file where
# it should appear only once). See also the "--disable" option for examples.
#enable=
# Disable the message, report, category or checker with the given id(s). You
# can either give multiple identifiers separated by comma (,) or put this
# option multiple times (only on the command line, not in the configuration
# file where it should appear only once).You can also use "--disable=all" to
# disable everything first and then re-enable specific checks. For example, if
# you want to run only the similarities checker, you can use "--disable=all
# --enable=similarities". If you want to run only the classes checker, but have
# no Warning level messages displayed, use"--disable=all --enable=classes
# --disable=W"
disable=R,
        abstract-method,
        apply-builtin,
        arguments-differ,
        attribute-defined-outside-init,
        backtick,
        bad-option-value,
        basestring-builtin,
        buffer-builtin,
        c-extension-no-member,
        consider-using-enumerate,
        cmp-builtin,
        cmp-method,
        coerce-builtin,
        coerce-method,
        delslice-method,
        div-method,
        eq-without-hash,
        execfile-builtin,
        file-builtin,
        filter-builtin-not-iterating,
        fixme,
        getslice-method,
        global-statement,
        hex-method,
        idiv-method,
        implicit-str-concat,
        import-error,
        import-self,
        import-star-module-level,
        import-outside-toplevel,
        input-builtin,
        intern-builtin,
        invalid-str-codec,
        locally-disabled,
        long-builtin,
        long-suffix,
        map-builtin-not-iterating,
        misplaced-comparison-constant,
        missing-function-docstring,
        metaclass-assignment,
        next-method-called,
        next-method-defined,
        no-absolute-import,
        no-init,  # added
        no-member,
        no-name-in-module,
        no-self-use,
        nonzero-method,
        oct-method,
        old-division,
        old-ne-operator,
        old-octal-literal,
        old-raise-syntax,
        parameter-unpacking,
        print-statement,
        raising-string,
        range-builtin-not-iterating,
        raw_input-builtin,
        rdiv-method,
        reduce-builtin,
        relative-import,
        reload-builtin,
        round-builtin,
        setslice-method,
        signature-differs,
        standarderror-builtin,
        suppressed-message,
        sys-max-int,
        trailing-newlines,
        unichr-builtin,
        unicode-builtin,
        unnecessary-pass,
        unpacking-in-except,
        useless-else-on-loop,
        useless-suppression,
        using-cmp-argument,
        wrong-import-order,
        xrange-builtin,
        zip-builtin-not-iterating,
[REPORTS]
# Set the output format. Available formats are text, parseable, colorized, msvs
# (visual studio) and html. You can also give a reporter class, eg
# mypackage.mymodule.MyReporterClass.
output-format=text
# Tells whether to display a full report or only the messages
reports=no
# Python expression which should return a note less than 10 (10 is the highest
# note). You have access to the variables errors warning, statement which
# respectively contain the number of errors / warnings messages and the total
# number of statements analyzed. This is used by the global evaluation report
# (RP0004).
evaluation=10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)
# Template used to display messages. This is a python new-style format string
# used to format the message information. See doc for all details
#msg-template=
[BASIC]
# Good variable names which should always be accepted, separated by a comma
good-names=main,_
# Bad variable names which should always be refused, separated by a comma
bad-names=
# Colon-delimited sets of names that determine each other's naming style when
# the name regexes allow several styles.
name-group=
# Include a hint for the correct naming format with invalid-name
include-naming-hint=no
# List of decorators that produce properties, such as abc.abstractproperty. Add
# to this list to register other decorators that produce valid properties.
property-classes=abc.abstractproperty,cached_property.cached_property,cached_property.threaded_cached_property,cached_property.cached_property_with_ttl,cached_property.threaded_cached_property_with_ttl
# Regular expression matching correct function names
function-rgx=^(?:(?P<exempt>setUp|tearDown|setUpModule|tearDownModule)|(?P<camel_case>_?[A-Z][a-zA-Z0-9]*)|(?P<snake_case>_?[a-z][a-z0-9_]*))$
# Regular expression matching correct variable names
variable-rgx=^[a-z][a-z0-9_]*$
# Regular expression matching correct constant names
const-rgx=^(_?[A-Z][A-Z0-9_]*|__[a-z0-9_]+__|_?[a-z][a-z0-9_]*)$
# Regular expression matching correct attribute names
attr-rgx=^_{0,2}[a-z][a-z0-9_]*$
# Regular expression matching correct argument names
argument-rgx=^[a-z][a-z0-9_]*$
# Regular expression matching correct class attribute names
class-attribute-rgx=^(_?[A-Z][A-Z0-9_]*|__[a-z0-9_]+__|_?[a-z][a-z0-9_]*)$
# Regular expression matching correct inline iteration names
inlinevar-rgx=^[a-z][a-z0-9_]*$
# Regular expression matching correct class names
class-rgx=^_?[A-Z][a-zA-Z0-9]*$
# Regular expression matching correct module names
module-rgx=^(_?[a-z][a-z0-9_]*|__init__)$
# Regular expression matching correct method names
# Regular expression which should only match function or class names that do
# not require a docstring.
# Minimum line length for functions/classes that require docstrings, shorter
# ones are exempt.
docstring-min-length=12
[TYPECHECK]
# List of decorators that produce context managers, such as
# contextlib.contextmanager. Add to this list to register other decorators that
# produce valid context managers.
contextmanager-decorators=contextlib.contextmanager,contextlib2.contextmanager
# List of module names for which member attributes should not be checked
# (useful for modules/projects where namespaces are manipulated during runtime
# and thus existing member attributes cannot be deduced by static analysis. It
# supports qualified module names, as well as Unix pattern matching.
ignored-modules=
# List of class names for which member attributes should not be checked (useful
# for classes with dynamically set attributes). This supports the use of
# qualified names.
ignored-classes=optparse.Values,thread._local,_thread._local
# List of members which are set dynamically and missed by pylint inference
# system, and so shouldn't trigger E1101 when accessed. Python regular
# expressions are accepted.
generated-members=
[FORMAT]
# Maximum number of characters on a single line.
max-line-length=80
# lines made too long by directives to pytype.
# Regexp for a line that is allowed to be longer than the limit.
ignore-long-lines=(?x)(
  ^\s*(\#\ )?<?https?://\S+>?$|
  ^\s*(from\s+\S+\s+)?import\s+.+$)
# else.
single-line-if-stmt=yes
# Maximum number of lines in a module
max-module-lines=99999
# String used as indentation unit.  The internal Google style guide mandates 2
# spaces.  Google's externaly-published style guide says 4, consistent with
# PEP 8.  Here, we use 2 spaces, for conformity with many open-sourced Google
# projects (like TensorFlow).
indent-string='  '
# Number of spaces of indent required inside a hanging  or continued line.
indent-after-paren=4
# Expected format of line ending, e.g. empty (any line ending), LF or CRLF.
expected-line-ending-format=
[MISCELLANEOUS]
# List of note tags to take in consideration, separated by a comma.
notes=TODO
[STRING]
# This flag controls whether inconsistent-quotes generates a warning when the
# character used as a quote delimiter is used inconsistently within a module.
check-quote-consistency=yes
[VARIABLES]
# Tells whether we should check for unused import in __init__ files.
init-import=no
# A regular expression matching the name of dummy variables (i.e. expectedly
# not used).
dummy-variables-rgx=^\*{0,2}(_$|unused_|dummy_)
# List of additional names supposed to be defined in builtins. Remember that
# you should avoid to define new builtins when possible.
additional-builtins=
# List of strings which can identify a callback function by name. A callback
# name must start or end with one of those strings.
callbacks=cb_,_cb
# List of qualified module names which can have objects that can redefine
# builtins.
redefining-builtins-modules=six,six.moves,past.builtins,future.builtins,functools
[LOGGING]
# Logging modules to check that the string format arguments are in logging
# function parameter format
logging-modules=logging,absl.logging,tensorflow.io.logging
[SIMILARITIES]
# Minimum lines number of a similarity.
min-similarity-lines=4
# Ignore comments when computing similarities.
ignore-comments=yes
# Ignore docstrings when computing similarities.
ignore-docstrings=yes
# Ignore imports when computing similarities.
ignore-imports=no
[SPELLING]
# Spelling dictionary name. Available dictionaries: none. To make it working
# install python-enchant package.
spelling-dict=
# List of comma separated words that should not be checked.
spelling-ignore-words=
# A path to a file that contains private dictionary; one word per line.
spelling-private-dict-file=
# Tells whether to store unknown words to indicated private dictionary in
# --spelling-private-dict-file option instead of raising a message.
spelling-store-unknown-words=no
[IMPORTS]
# Deprecated modules which should not be used, separated by a comma
deprecated-modules=regsub,
                   TERMIOS,
                   Bastion,
                   rexec,
                   sets
# Create a graph of every (i.e. internal and external) dependencies in the
# given file (report RP0402 must not be disabled)
import-graph=
# Create a graph of external dependencies in the given file (report RP0402 must
# not be disabled)
ext-import-graph=
# Create a graph of internal dependencies in the given file (report RP0402 must
# not be disabled)
int-import-graph=
# Force import order to recognize a module as part of the standard
# compatibility libraries.
known-standard-library=
# Force import order to recognize a module as part of a third party library.
known-third-party=enchant, absl
# Analyse import fallback blocks. This can be used to support both Python 2 and
# 3 compatible code, which means that the block might have code that exists
# only in one or another interpreter, leading to false positives when analysed.
analyse-fallback-blocks=no
[CLASSES]
# List of method names used to declare (i.e. assign) instance attributes.
defining-attr-methods=__init__,
                      __new__,
                      setUp
# List of member names, which should be excluded from the protected access
# warning.
exclude-protected=_asdict,
                  _fields,
                  _replace,
                  _source,
                  _make
# List of valid names for the first argument in a class method.
valid-classmethod-first-arg=cls,
                            class_
# List of valid names for the first argument in a metaclass class method.
valid-metaclass-classmethod-first-arg=mcs
================================================
================================================
[project]
# Project metadata. Available keys are documented at:
name = "google-adk"
description = "Agent Development Kit"
requires-python = ">=3.9"
authors = [{ name = "Google LLC", email = "googleapis-packages@google.com" }]
classifiers = [ # List of https://pypi.org/classifiers/
  "Typing :: Typed",
  "Intended Audience :: Developers",
  "Intended Audience :: Science/Research",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Operating System :: OS Independent",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "License :: OSI Approved :: Apache Software License",
]
dependencies = [
  # go/keep-sorted start
  "authlib>=1.5.1",                                  # For RestAPI Tool
  "click>=8.1.8",                                    # For CLI tools
  "fastapi>=0.115.0",                                # FastAPI framework
  "google-api-python-client>=2.157.0",               # Google API client discovery
  "google-cloud-aiplatform[agent_engines]>=1.95.1",  # For VertexAI integrations, e.g. example store.
  "google-cloud-secret-manager>=2.22.0",             # Fetching secrets in RestAPI Tool
  "google-cloud-speech>=2.30.0",                     # For Audio Transcription
  "google-cloud-storage>=2.18.0, <3.0.0",            # For GCS Artifact service
  "google-genai>=1.17.0",                            # Google GenAI SDK
  "graphviz>=0.20.2",                                # Graphviz for graph rendering
  "mcp>=1.8.0;python_version>='3.10'",               # For MCP Toolset
  "opentelemetry-api>=1.31.0",                       # OpenTelemetry
  "opentelemetry-exporter-gcp-trace>=1.9.0",
  "opentelemetry-sdk>=1.31.0",
  "pydantic>=2.0, <3.0.0",                           # For data validation/models
  "python-dotenv>=1.0.0",                            # To manage environment variables
  "PyYAML>=6.0.2",                                   # For APIHubToolset.
  "sqlalchemy>=2.0",                                 # SQL database ORM
  "tzlocal>=5.3",                                    # Time zone utilities
  "uvicorn>=0.34.0",                                 # ASGI server for FastAPI
  # go/keep-sorted end
]
dynamic = ["version"]
[project.urls]
[project.scripts]
adk = "google.adk.cli:main"
[project.optional-dependencies]
dev = [
  # go/keep-sorted start
  "flit>=3.10.0",
  "isort>=6.0.0",
  "pyink>=24.10.0",
  "pylint>=2.6.0",
  "mypy>=1.15.0",
  # go/keep-sorted end
]
eval = [
  # go/keep-sorted start
  "google-cloud-aiplatform[evaluation]>=1.87.0",
  "pandas>=2.2.3",
  "tabulate>=0.9.0",
  # go/keep-sorted end
]
  # go/keep-sorted start
  "langchain-community>=0.3.17",
  "langgraph>=0.2.60",               # For LangGraphAgent
  # go/keep-sorted end
]
docs = [
  "autodoc_pydantic",
  "furo",
  "myst-parser",
  "sphinx",
  "sphinx-autodoc-typehints",
  "sphinx-rtd-theme",
]
# Optional extensions
extensions = [
  "anthropic>=0.43.0",                    # For anthropic model support
  "beautifulsoup4>=3.2.2",                # For load_web_page tool.
  "crewai[tools];python_version>='3.10'", # For CrewaiTool
  "langgraph>=0.2.60",                    # For LangGraphAgent
  "litellm>=1.63.11",                     # For LiteLLM support
  "llama-index-readers-file>=0.4.0",      # For retrieval using LlamaIndex.
  "lxml>=5.3.0",                          # For load_web_page tool.
  "toolbox-core>=0.1.0",                  # For tools.toolbox_toolset.ToolboxToolset
]
[tool.pyink]
# Format py files following Google style-guide
line-length = 80
unstable = true
pyink-indentation = 2
pyink-use-majority-quotes = true
pyink-annotation-pragmas = [
  "noqa",
  "pylint:",
  "type: ignore",
  "pytype:",
  "mypy:",
  "pyright:",
  "pyre-",
]
[build-system]
# Build system specify which backend is used to build/install the project (flit,
# poetry, setuptools,...). All backends are supported by `pip install`
requires = ["flit_core >=3.8,<4"]
build-backend = "flit_core.buildapi"
[tool.flit.sdist]
exclude = ['src/**/*.sh']
[tool.flit.module]
name = "google.adk"
include = ["py.typed"]
[tool.isort]
profile = "google"
single_line_exclusions = []
known_third_party = ["google.adk"]
asyncio_default_fixture_loop_scope = "function"
asyncio_mode = "auto"
[tool.mypy]
python_version = "3.9"
plugins = ["pydantic.mypy"]
# Start with non-strict mode, and swtich to strict mode later.
# strict = true
disable_error_code = ["import-not-found", "import-untyped", "unused-ignore"]
follow_imports = "skip"
================================================
================================================
# Contributing Resources
# Samples
================================================
================================================
# Application Integration Agent Sample
## Introduction
This sample demonstrates how to use the `ApplicationIntegrationToolset` within an ADK agent to interact with external applications, specifically Jira in this case. The agent (`agent.py`) is configured to manage Jira issues using a pre-configured Application Integration connection.
## Prerequisites
1.  **Set up Integration Connection:**
    * 
2.  **Configure Environment Variables:**
    *   Create a `.env` file in the same directory as `agent.py` (or add to your existing one).
    *   Add the following variables to the `.env` file, replacing the placeholder values with your actual connection details:
      ```dotenv
      CONNECTION_NAME=<YOUR_JIRA_CONNECTION_NAME>
      CONNECTION_LOCATION=<YOUR_CONNECTION_LOCATION>
      ```
## How to Use
1.  **Install Dependencies:** Ensure you have the necessary libraries installed (e.g., `google-adk`, `python-dotenv`).
2.  **Run the Agent:** Execute the agent script from your terminal:
    ```bash
    python agent.py
    ```
3.  **Interact:** Once the agent starts, you can interact with it by typing prompts related to Jira issue management.
## Sample Prompts
Here are some examples of how you can interact with the agent:
*   `Can you list me all the issues ?`
*   `Can you list me all the projects ?`
*   `Can you create an issue: "Bug in product XYZ" in project ABC ?`
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Sample agent using Application Integration toolset."""
import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.application_integration_tool import ApplicationIntegrationToolset
# Load environment variables from .env file
load_dotenv()
connection_name = os.getenv("CONNECTION_NAME")
connection_location = os.getenv("CONNECTION_LOCATION")
jira_toolset = ApplicationIntegrationToolset(
    project=connection_project,
    location=connection_location,
    connection=connection_name,
    entity_operations={"Issues": [], "Projects": []},
    tool_name_prefix="jira_issue_manager",
)
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="Issue_Management_Agent",
    instruction="""
    You are an agent that helps manage issues in a JIRA instance.
    Be accurate in your responses based on the tool response. You can perform any formatting in the response that is appropriate or if asked by the user.
    If there is an error in the tool response, understand the error and try and see if you can fix the error and then  and execute the tool again. For example if a variable or parameter is missing, try and see if you can find it in the request or user query or default it and then execute the tool again or check for other tools that could give you the details.
    If there are any math operations like count or max, min in the user request, call the tool to get the data and perform the math operations and then return the result in the response. For example for maximum, fetch the list and then do the math operation.
    """,
    tools=[jira_toolset],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
async def log_query(tool_context: ToolContext, query: str):
    """Saves the provided query string as a 'text/plain' artifact named 'query'."""
    query_bytes = query.encode('utf-8')
    artifact_part = types.Part(
      inline_data=types.Blob(
          mime_type='text/plain',
          data=query_bytes
      )
    )
    await tool_context.save_artifact('query', artifact_part)
root_agent = Agent(
    model='gemini-2.0-flash',
    name='log_agent',
    description='Log user query.',
    instruction="""Always log the user query and reploy "kk, I've logged."
    """,
    tools=[log_query],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
================================================
================================================
# BigQuery Tools Sample
## Introduction
This sample agent demonstrates the BigQuery first-party tools in ADK,
distributed via the `google.adk.tools.bigquery` module. These tools include:
1. `list_dataset_ids`
  Fetches BigQuery dataset ids present in a GCP project.
1. `get_dataset_info`
  Fetches metadata about a BigQuery dataset.
1. `list_table_ids`
  Fetches table ids present in a BigQuery dataset.
1. `get_table_info`
  Fetches metadata about a BigQuery table.
1. `execute_sql`
  Runs a SQL query in BigQuery.
## How to use
Set up environment variables in your `.env` file for using
or
for the LLM service for your agent. For example, for using Google AI Studio you
would set:
* GOOGLE_GENAI_USE_VERTEXAI=FALSE
* GOOGLE_API_KEY={your api key}
### With Application Default Credentials
This mode is useful for quick development when the agent builder is the only
user interacting with the agent. The tools are initialized with the default
credentials present on the machine running the agent.
1. Create application default credentials on the machine where the agent would
be running by following https://cloud.google.com/docs/authentication/provide-credentials-adc.
1. Set `RUN_WITH_ADC=True` in `agent.py` and run the agent
### With Interactive OAuth
1. Follow
https://developers.google.com/identity/protocols/oauth2#1.-obtain-oauth-2.0-credentials-from-the-dynamic_data.setvar.console_name.
to get your client id and client secret. Be sure to choose "web" as your client
type.
1. Follow https://developers.google.com/workspace/guides/configure-oauth-consent to add scope "https://www.googleapis.com/auth/bigquery".
1. Follow https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred to add http://localhost/dev-ui/ to "Authorized redirect URIs".
  Note: localhost here is just a hostname that you use to access the dev ui,
  replace it with the actual hostname you use to access the dev ui.
1. For 1st run, allow popup for localhost in Chrome.
1. Configure your `.env` file to add two more variables before running the agent:
  * OAUTH_CLIENT_ID={your client id}
  * OAUTH_CLIENT_SECRET={your client secret}
  Note: don't create a separate .env, instead put it to the same .env file that
  stores your Vertex AI or Dev ML credentials
1. Set `RUN_WITH_ADC=False` in `agent.py` and run the agent
## Sample prompts
* which weather datasets exist in bigquery public data?
* tell me more about noaa_lightning
* which tables exist in the ml_datasets dataset?
* show more details about the penguins table
* compute penguins population per island.
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from google.adk.agents import llm_agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
import google.auth
RUN_WITH_ADC = False
if RUN_WITH_ADC:
  # Initialize the tools to use the application default credentials.
  application_default_credentials, _ = google.auth.default()
  credentials_config = BigQueryCredentialsConfig(
      credentials=application_default_credentials
  )
else:
  # Initiaze the tools to do interactive OAuth
  # The environment variables OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET
  # must be set
  credentials_config = BigQueryCredentialsConfig(
      client_id=os.getenv("OAUTH_CLIENT_ID"),
      client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
  )
bigquery_toolset = BigQueryToolset(credentials_config=credentials_config)
# The variable name `root_agent` determines what your root agent is for the
# debug CLI
root_agent = llm_agent.Agent(
    model="gemini-2.0-flash",
    name="hello_agent",
    description=(
        "Agent to answer questions about BigQuery data and models and execute"
        " SQL queries."
    ),
    instruction="""\
        You are a data science agent with access to several BigQuery tools.
        Make use of those tools to answer the user's questions.
    """,
    tools=[bigquery_toolset],
)
================================================
================================================
# BigQuery Sample
## Introduction
* 1. bigquery_datasets_list:
    List user's datasets.
* 2. bigquery_datasets_get:
    Get a dataset's details.
* 3. bigquery_datasets_insert:
    Create a new dataset.
* 4. bigquery_tables_list:
    List all tables in a dataset.
* 5. bigquery_tables_get:
    Get a table's details.
* 6. bigquery_tables_insert:
    Insert a new table into a dataset.
## How to use
* 1. Follow https://developers.google.com/identity/protocols/oauth2#1.-obtain-oauth-2.0-credentials-from-the-dynamic_data.setvar.console_name. to get your client id and client secret.
  Be sure to choose "web" as your client type.
* 2. Configure your `.env` file to add two variables:
  * OAUTH_CLIENT_ID={your client id}
  * OAUTH_CLIENT_SECRET={your client secret}
  Note: don't create a separate `.env` file , instead put it to the same `.env` file that stores your Vertex AI or Dev ML credentials
* 3. Follow https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred to add http://localhost/dev-ui/ to "Authorized redirect URIs".
  Note: localhost here is just a hostname that you use to access the dev ui, replace it with the actual hostname you use to access the dev ui.
* 4. For 1st run, allow popup for localhost in Chrome.
## Sample prompt
* `Do I have any datasets in project sean-dev-agent ?`
* `Do I have any tables under it ?`
* `could you get me the details of this table ?`
* `could you show me the details of this new dataset ?`
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools.google_api_tool import BigQueryToolset
# Load environment variables from .env file
load_dotenv()
# Access the variable
oauth_client_id = os.getenv("OAUTH_CLIENT_ID")
oauth_client_secret = os.getenv("OAUTH_CLIENT_SECRET")
tools_to_expose = [
    "bigquery_datasets_list",
    "bigquery_datasets_get",
    "bigquery_datasets_insert",
    "bigquery_tables_list",
    "bigquery_tables_get",
    "bigquery_tables_insert",
]
bigquery_toolset = BigQueryToolset(
    client_id=oauth_client_id,
    client_secret=oauth_client_secret,
    tool_filter=tools_to_expose,
)
root_agent = Agent(
    model="gemini-2.0-flash",
    name="bigquery_agent",
    instruction="""
      You are a helpful Google BigQuery agent that help to manage users' data on Google BigQuery.
      Use the provided tools to conduct various operations on users' data in Google BigQuery.
      Scenario 1:
      The user wants to query their biguqery datasets
      Use bigquery_datasets_list to query user's datasets
      Scenario 2:
      The user wants to query the details of a specific dataset
      Use bigquery_datasets_get to get a dataset's details
      Scenario 3:
      The user wants to create a new dataset
      Use bigquery_datasets_insert to create a new dataset
      Scenario 4:
      The user wants to query their tables in a specific dataset
      Use bigquery_tables_list to list all tables in a dataset
      Scenario 5:
      The user wants to query the details of a specific table
      Use bigquery_tables_get to get a table's details
      Scenario 6:
      The user wants to insert a new table into a dataset
      Use bigquery_tables_insert to insert a new table into a dataset
      Current user:
      <User>
      {userInfo?}
      </User>
""",
    tools=[bigquery_toolset],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
def roll_die(sides: int, tool_context: ToolContext) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  result = random.randint(1, sides)
  if not 'rolls' in tool_context.state:
    tool_context.state['rolls'] = []
  tool_context.state['rolls'] = tool_context.state['rolls'] + [result]
  return result
async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.
  Args:
    nums: The list of numbers to check.
  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
async def before_agent_callback(callback_context):
  print('@before_agent_callback')
  return None
async def after_agent_callback(callback_context):
  print('@after_agent_callback')
  return None
async def before_model_callback(callback_context, llm_request):
  print('@before_model_callback')
  return None
async def after_model_callback(callback_context, llm_response):
  print('@after_model_callback')
  return None
def after_agent_cb1(callback_context):
  print('@after_agent_cb1')
def after_agent_cb2(callback_context):
  print('@after_agent_cb2')
  # ModelContent (or Content with role set to 'model') must be returned.
  # Otherwise, the event will be excluded from the context in the next turn.
  return types.ModelContent(
      parts=[
          types.Part(
              text='(stopped) after_agent_cb2',
          ),
      ],
  )
def after_agent_cb3(callback_context):
  print('@after_agent_cb3')
def before_agent_cb1(callback_context):
  print('@before_agent_cb1')
def before_agent_cb2(callback_context):
  print('@before_agent_cb2')
def before_agent_cb3(callback_context):
  print('@before_agent_cb3')
def before_tool_cb1(tool, args, tool_context):
  print('@before_tool_cb1')
def before_tool_cb2(tool, args, tool_context):
  print('@before_tool_cb2')
def before_tool_cb3(tool, args, tool_context):
  print('@before_tool_cb3')
def after_tool_cb1(tool, args, tool_context, tool_response):
  print('@after_tool_cb1')
def after_tool_cb2(tool, args, tool_context, tool_response):
  print('@after_tool_cb2')
def after_tool_cb3(tool, args, tool_context, tool_response):
  print('@after_tool_cb3')
root_agent = Agent(
    model='gemini-2.0-flash',
    name='data_processing_agent',
    description=(
        'hello world agent that can roll a dice of 8 sides and check prime'
        ' numbers.'
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #     ),
    # ),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
    before_agent_callback=[
        before_agent_cb1,
        before_agent_cb2,
        before_agent_cb3,
    ],
    after_agent_callback=[after_agent_cb1, after_agent_cb2, after_agent_cb3],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    before_tool_callback=[before_tool_cb1, before_tool_cb2, before_tool_cb3],
    after_tool_callback=[after_tool_cb1, after_tool_cb2, after_tool_cb3],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
import warnings
import agent
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
warnings.filterwarnings('ignore', category=UserWarning)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  session_service = InMemorySessionService()
  artifact_service = InMemoryArtifactService()
  runner = Runner(
      app_name=app_name,
      agent=agent.root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  session_11 = await session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi')
  await run_prompt(session_11, 'Roll a die with 100 sides')
  await run_prompt(session_11, 'Roll a die again with 100 sides.')
  await run_prompt(session_11, 'What numbers did I got?')
  print(
      await artifact_service.list_artifact_keys(
          app_name=app_name, user_id=user_id_1, session_id=session_11.id
      )
  )
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Data science agent."""
from google.adk.agents.llm_agent import Agent
from google.adk.code_executors.built_in_code_executor import BuiltInCodeExecutor
def base_system_instruction():
  """Returns: data science agent system instruction."""
  return """
  # Guidelines
  **Objective:** Assist the user in achieving their data analysis goals within the context of a Python Colab notebook, **with emphasis on avoiding assumptions and ensuring accuracy.** Reaching that goal can involve multiple steps. When you need to generate code, you **don't** need to solve the goal in one go. Only generate the next step at a time.
  **Code Execution:** All code snippets provided will be executed within the Colab environment.
  **Statefulness:** All code snippets are executed and the variables stays in the environment. You NEVER need to re-initialize variables. You NEVER need to reload files. You NEVER need to re-import libraries.
  **Imported Libraries:** The following libraries are ALREADY imported and should NEVER be imported again:
  ```tool_code
  import io
  import math
  import re
  import matplotlib.pyplot as plt
  import numpy as np
  import pandas as pd
  import scipy
  ```
  **Output Visibility:** Always print the output of code execution to visualize results, especially for data exploration and analysis. For example:
    - To look a the shape of a pandas.DataFrame do:
      ```tool_code
      print(df.shape)
      ```
      The output will be presented to you as:
      ```tool_outputs
      (49, 7)
      ```
    - To display the result of a numerical computation:
      ```tool_code
      x = 10 ** 9 - 12 ** 5
      print(f'{{x=}}')
      ```
      The output will be presented to you as:
      ```tool_outputs
      x=999751168
      ```
    - You **never** generate ```tool_outputs yourself.
    - You can then use this output to decide on next steps.
    - Print just variables (e.g., `print(f'{{variable=}}')`.
  **No Assumptions:** **Crucially, avoid making assumptions about the nature of the data or column names.** Base findings solely on the data itself. Always use the information obtained from `explore_df` to guide your analysis.
  **Available files:** Only use the files that are available as specified in the list of available files.
  **Data in prompt:** Some queries contain the input data directly in the prompt. You have to parse that data into a pandas DataFrame. ALWAYS parse all the data. NEVER edit the data that are given to you.
  **Answerability:** Some queries may not be answerable with the available data. In those cases, inform the user why you cannot process their query and suggest what type of data would be needed to fulfill their request.
  """
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="data_science_agent",
    instruction=base_system_instruction() + """
You need to assist the user with their queries by looking at the data and the context in the conversation.
You final answer should summarize the code and code execution relavant to the user query.
You should include all pieces of data to answer the user query, such as the table from code execution results.
If you cannot answer the question directly, you should follow the guidelines above to generate the next step.
If the question can be answered directly with writing any code, you should do that.
If you doesn't have enough data to answer the question, you should ask for clarification from the user.
You should NEVER install any package on your own like `pip install ...`.
When plotting trends, you should make sure to sort and order the data by the x-axis.
""",
    code_executor=BuiltInCodeExecutor(),
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk import Agent
from pydantic import BaseModel
class WeahterData(BaseModel):
  temperature: str
  humidity: str
  wind_speed: str
root_agent = Agent(
    name='root_agent',
    model='gemini-2.0-flash',
    instruction="""\
Answer user's questions based on the data you have.
If you don't have the data, you can just say you don't know.
Here are the data you have for San Jose
* temperature: 26 C
* humidity: 20%
* wind_speed: 29 mph
Here are the data you have for Cupertino
* temperature: 16 C
* humidity: 10%
* wind_speed: 13 mph
""",
    output_schema=WeahterData,
    output_key='weather_data',
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
def roll_die(sides: int, tool_context: ToolContext) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  result = random.randint(1, sides)
  if not 'rolls' in tool_context.state:
    tool_context.state['rolls'] = []
  tool_context.state['rolls'] = tool_context.state['rolls'] + [result]
  return result
async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.
  Args:
    nums: The list of numbers to check.
  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
root_agent = Agent(
    model='gemini-2.5-pro-preview-03-25',
    # model='gemini-2.0-flash',
    name='data_processing_agent',
    description=(
        'hello world agent that can roll a dice of 8 sides and check prime'
        ' numbers.'
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
        ),
    ),
    # planner=PlanReActPlanner(),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
import warnings
import agent
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
warnings.filterwarnings('ignore', category=UserWarning)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  session_service = InMemorySessionService()
  artifact_service = InMemoryArtifactService()
  runner = Runner(
      app_name=app_name,
      agent=agent.root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  session_11 = await session_service.create_session(app_name, user_id_1)
  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi')
  await run_prompt(session_11, 'Roll a die.')
  await run_prompt(session_11, 'Roll a die again.')
  await run_prompt(session_11, 'What numbers did I got?')
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.genai import Client
from google.genai import types
from google.adk import Agent
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
# Only Vertex AI supports image generation for now.
client = Client()
async def generate_image(prompt: str, tool_context: 'ToolContext'):
  """Generates an image based on the prompt."""
  response = client.models.generate_images(
      model='imagen-3.0-generate-002',
      prompt=prompt,
      config={'number_of_images': 1},
  )
  if not response.generated_images:
    return {'status': 'failed'}
  image_bytes = response.generated_images[0].image.image_bytes
  await tool_context.save_artifact(
      'image.png',
      types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
  )
  return {
      'status': 'success',
      'detail': 'Image generated successfully and stored in artifacts.',
      'filename': 'image.png',
  }
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description="""An agent that generates images and answer questions about the images.""",
    instruction="""You are an agent whose job is to generate or edit an image based on the user's prompt.
""",
    tools=[generate_image, load_artifacts],
)
================================================
================================================
{
  "id": "xtgNTCtR",
  "context": {
    "_time": "2024-11-05 22:34:22.483577"
  },
  "events": [
    {
      "invocation_id": "CFs9iCdD",
      "author": "user",
      "content": {
        "parts": [
          {
            "text": "a dog"
          }
        ],
        "role": "user"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {},
        "partial": false,
        "pending": false
      },
      "id": "LaWhnoSs",
      "type": "content",
      "timestamp": 1730874845.9344919
    },
    {
      "invocation_id": "CFs9iCdD",
      "author": "root_agent",
      "content": {
        "parts": [
          {
            "function_call": {
              "args": {
                "prompt": "a dog"
              },
              "name": "generate_image"
            }
          }
        ],
        "role": "model"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {},
        "partial": false,
        "pending": false
      },
      "id": "urXUWHfc",
      "type": "function_call",
      "timestamp": 1730874850.6203258
    },
    {
      "invocation_id": "CFs9iCdD",
      "author": "root_agent",
      "content": {
        "parts": [
          {
            "function_response": {
              "name": "generate_image",
              "response": {
                "status": "ok"
              }
            }
          }
        ],
        "role": "user"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {
          "image.png": {
            "inline_data": {
              "mime_type": "image/png"
            }
          }
        },
        "partial": false,
        "pending": false,
        "function_call_event_id": "urXUWHfc"
      },
      "id": "v92aRpZL",
      "type": "function_response",
      "timestamp": 1730874850.6219532
    },
    {
      "invocation_id": "CFs9iCdD",
      "author": "root_agent",
      "content": {
        "parts": [
          {
            "text": "OK. I have generated an image of a dog. \n"
          }
        ],
        "role": "model"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {},
        "partial": false,
        "pending": false
      },
      "id": "vxNenxyu",
      "type": "content",
      "timestamp": 1730874850.9896104
    },
    {
      "invocation_id": "IGkazcuO",
      "author": "user",
      "content": {
        "parts": [
          {
            "text": "add a duck"
          }
        ],
        "role": "user"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {},
        "partial": false,
        "pending": false
      },
      "id": "SDVijPil",
      "type": "content",
      "timestamp": 1730874854.9803195
    },
    {
      "invocation_id": "IGkazcuO",
      "author": "root_agent",
      "content": {
        "parts": [
          {
            "function_call": {
              "args": {
                "prompt": "a dog and a duck"
              },
              "name": "generate_image"
            }
          }
        ],
        "role": "model"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {},
        "partial": false,
        "pending": false
      },
      "id": "fqFlqdNL",
      "type": "function_call",
      "timestamp": 1730874858.7940624
    },
    {
      "invocation_id": "IGkazcuO",
      "author": "root_agent",
      "content": {
        "parts": [
          {
            "function_response": {
              "name": "generate_image",
              "response": {
                "status": "ok"
              }
            }
          }
        ],
        "role": "user"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {
          "image.png": {
            "inline_data": {
              "mime_type": "image/png"
            }
          }
        },
        "partial": false,
        "pending": false,
        "function_call_event_id": "fqFlqdNL"
      },
      "id": "WUyMzRsh",
      "type": "function_response",
      "timestamp": 1730874858.7951808
    },
    {
      "invocation_id": "IGkazcuO",
      "author": "root_agent",
      "content": {
        "parts": [
          {
            "text": "OK. I have generated an image of a dog and a duck. \n"
          }
        ],
        "role": "model"
      },
      "options": {
        "skip_summarization": false,
        "update_context": {},
        "update_artifact": {},
        "partial": false,
        "pending": false
      },
      "id": "WD2LHmFA",
      "type": "content",
      "timestamp": 1730874859.2492816
    }
  ],
  "past_events": [],
  "pending_events": {},
  "artifacts": {
    "image.png": [
      {
        "inline_data": {
          "mime_type": "image/png"
        }
      },
      {
        "inline_data": {
          "mime_type": "image/png"
        }
      }
    ]
  },
  "event_logs": [
    {
      "invocation_id": "CFs9iCdD",
      "event_id": "urXUWHfc",
      "model_request": {
        "model": "gemini-1.5-flash",
        "contents": [
          {
            "parts": [
              {
                "text": "a dog"
              }
            ],
            "role": "user"
          }
        ],
        "config": {
          "system_instruction": "You are an agent. Your name is root_agent.\nYou are an agent whose job is to generate or edit an image based on the user's prompt.\n",
          "tools": [
            {
              "function_declarations": [
                {
                  "parameters": {
                    "type": "OBJECT",
                    "properties": {
                      "prompt": {
                        "type": "STRING"
                      }
                    }
                  },
                  "description": "Generates an image based on the prompt.",
                  "name": "generate_image"
                }
              ]
            }
          ]
        }
      },
      "model_response": {
        "candidates": [
          {
            "content": {
              "parts": [
                {
                  "function_call": {
                    "args": {
                      "prompt": "a dog"
                    },
                    "name": "generate_image"
                  }
                }
              ],
              "role": "model"
            },
            "finish_reason": "STOP",
            "index": 0,
            "safety_ratings": [
              {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "probability": "NEGLIGIBLE"
              },
              {
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HARASSMENT",
                "probability": "NEGLIGIBLE"
              }
            ]
          }
        ],
        "model_version": "gemini-1.5-flash-001",
        "usage_metadata": {
          "candidates_token_count": 16,
          "prompt_token_count": 84,
          "total_token_count": 100
        }
      }
    },
    {
      "invocation_id": "CFs9iCdD",
      "event_id": "vxNenxyu",
      "model_request": {
        "model": "gemini-1.5-flash",
        "contents": [
          {
            "parts": [
              {
                "text": "a dog"
              }
            ],
            "role": "user"
          },
          {
            "parts": [
              {
                "function_call": {
                  "args": {
                    "prompt": "a dog"
                  },
                  "name": "generate_image"
                }
              }
            ],
            "role": "model"
          },
          {
            "parts": [
              {
                "function_response": {
                  "name": "generate_image",
                  "response": {
                    "status": "ok"
                  }
                }
              }
            ],
            "role": "user"
          }
        ],
        "config": {
          "system_instruction": "You are an agent. Your name is root_agent.\nYou are an agent whose job is to generate or edit an image based on the user's prompt.\n",
          "tools": [
            {
              "function_declarations": [
                {
                  "parameters": {
                    "type": "OBJECT",
                    "properties": {
                      "prompt": {
                        "type": "STRING"
                      }
                    }
                  },
                  "description": "Generates an image based on the prompt.",
                  "name": "generate_image"
                }
              ]
            }
          ]
        }
      },
      "model_response": {
        "candidates": [
          {
            "content": {
              "parts": [
                {
                  "text": "OK. I have generated an image of a dog. \n"
                }
              ],
              "role": "model"
            },
            "finish_reason": "STOP",
            "index": 0,
            "safety_ratings": [
              {
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HARASSMENT",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "probability": "NEGLIGIBLE"
              }
            ]
          }
        ],
        "model_version": "gemini-1.5-flash-001",
        "usage_metadata": {
          "candidates_token_count": 11,
          "prompt_token_count": 117,
          "total_token_count": 128
        }
      }
    },
    {
      "invocation_id": "IGkazcuO",
      "event_id": "fqFlqdNL",
      "model_request": {
        "model": "gemini-1.5-flash",
        "contents": [
          {
            "parts": [
              {
                "text": "a dog"
              }
            ],
            "role": "user"
          },
          {
            "parts": [
              {
                "function_call": {
                  "args": {
                    "prompt": "a dog"
                  },
                  "name": "generate_image"
                }
              }
            ],
            "role": "model"
          },
          {
            "parts": [
              {
                "function_response": {
                  "name": "generate_image",
                  "response": {
                    "status": "ok"
                  }
                }
              }
            ],
            "role": "user"
          },
          {
            "parts": [
              {
                "text": "OK. I have generated an image of a dog. \n"
              }
            ],
            "role": "model"
          },
          {
            "parts": [
              {
                "text": "add a duck"
              }
            ],
            "role": "user"
          }
        ],
        "config": {
          "system_instruction": "You are an agent. Your name is root_agent.\nYou are an agent whose job is to generate or edit an image based on the user's prompt.\n",
          "tools": [
            {
              "function_declarations": [
                {
                  "parameters": {
                    "type": "OBJECT",
                    "properties": {
                      "prompt": {
                        "type": "STRING"
                      }
                    }
                  },
                  "description": "Generates an image based on the prompt.",
                  "name": "generate_image"
                }
              ]
            }
          ]
        }
      },
      "model_response": {
        "candidates": [
          {
            "content": {
              "parts": [
                {
                  "function_call": {
                    "args": {
                      "prompt": "a dog and a duck"
                    },
                    "name": "generate_image"
                  }
                }
              ],
              "role": "model"
            },
            "finish_reason": "STOP",
            "index": 0,
            "safety_ratings": [
              {
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HARASSMENT",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "probability": "NEGLIGIBLE"
              }
            ]
          }
        ],
        "model_version": "gemini-1.5-flash-001",
        "usage_metadata": {
          "candidates_token_count": 19,
          "prompt_token_count": 135,
          "total_token_count": 154
        }
      }
    },
    {
      "invocation_id": "IGkazcuO",
      "event_id": "WD2LHmFA",
      "model_request": {
        "model": "gemini-1.5-flash",
        "contents": [
          {
            "parts": [
              {
                "text": "a dog"
              }
            ],
            "role": "user"
          },
          {
            "parts": [
              {
                "function_call": {
                  "args": {
                    "prompt": "a dog"
                  },
                  "name": "generate_image"
                }
              }
            ],
            "role": "model"
          },
          {
            "parts": [
              {
                "function_response": {
                  "name": "generate_image",
                  "response": {
                    "status": "ok"
                  }
                }
              }
            ],
            "role": "user"
          },
          {
            "parts": [
              {
                "text": "OK. I have generated an image of a dog. \n"
              }
            ],
            "role": "model"
          },
          {
            "parts": [
              {
                "text": "add a duck"
              }
            ],
            "role": "user"
          },
          {
            "parts": [
              {
                "function_call": {
                  "args": {
                    "prompt": "a dog and a duck"
                  },
                  "name": "generate_image"
                }
              }
            ],
            "role": "model"
          },
          {
            "parts": [
              {
                "function_response": {
                  "name": "generate_image",
                  "response": {
                    "status": "ok"
                  }
                }
              }
            ],
            "role": "user"
          }
        ],
        "config": {
          "system_instruction": "You are an agent. Your name is root_agent.\nYou are an agent whose job is to generate or edit an image based on the user's prompt.\n",
          "tools": [
            {
              "function_declarations": [
                {
                  "parameters": {
                    "type": "OBJECT",
                    "properties": {
                      "prompt": {
                        "type": "STRING"
                      }
                    }
                  },
                  "description": "Generates an image based on the prompt.",
                  "name": "generate_image"
                }
              ]
            }
          ]
        }
      },
      "model_response": {
        "candidates": [
          {
            "content": {
              "parts": [
                {
                  "text": "OK. I have generated an image of a dog and a duck. \n"
                }
              ],
              "role": "model"
            },
            "finish_reason": "STOP",
            "index": 0,
            "safety_ratings": [
              {
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_HARASSMENT",
                "probability": "NEGLIGIBLE"
              },
              {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "probability": "NEGLIGIBLE"
              }
            ]
          }
        ],
        "model_version": "gemini-1.5-flash-001",
        "usage_metadata": {
          "candidates_token_count": 14,
          "prompt_token_count": 171,
          "total_token_count": 185
        }
      }
    }
  ]
}
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.genai import Client
from google.adk import Agent
from google.adk.tools import google_search
# Only Vertex AI supports image generation for now.
client = Client()
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description="""an agent whose job it is to perform Google search queries and answer questions about the results.""",
    instruction="""You are an agent whose job is to perform Google search queries and answer questions about the results.
""",
    tools=[google_search],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
def roll_die(sides: int, tool_context: ToolContext) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  result = random.randint(1, sides)
  if not 'rolls' in tool_context.state:
    tool_context.state['rolls'] = []
  tool_context.state['rolls'] = tool_context.state['rolls'] + [result]
  return result
async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.
  Args:
    nums: The list of numbers to check.
  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
root_agent = Agent(
    model='gemini-2.0-flash',
    name='data_processing_agent',
    description=(
        'hello world agent that can roll a dice of 8 sides and check prime'
        ' numbers.'
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #     ),
    # ),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
import agent
from dotenv import load_dotenv
from google.adk.agents.run_config import RunConfig
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  runner = InMemoryRunner(
      agent=agent.root_agent,
      app_name=app_name,
  )
  session_11 = await runner.session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  async def run_prompt_bytes(session: Session, new_message: str):
    content = types.Content(
        role='user',
        parts=[
            types.Part.from_bytes(
                data=str.encode(new_message), mime_type='text/plain'
            )
        ],
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
        run_config=RunConfig(save_input_blobs_as_artifacts=True),
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi')
  await run_prompt(session_11, 'Roll a die with 100 sides')
  await run_prompt(session_11, 'Roll a die again with 100 sides.')
  await run_prompt(session_11, 'What numbers did I got?')
  await run_prompt_bytes(session_11, 'Hi bytes')
  print(
      await runner.artifact_service.list_artifact_keys(
          app_name=app_name, user_id=user_id_1, session_id=session_11.id
      )
  )
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
def roll_die(sides: int) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  return random.randint(1, sides)
async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.
  Args:
    nums: The list of numbers to check.
  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      "No prime numbers found."
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
root_agent = Agent(
    # model=LiteLlm(model="gemini/gemini-2.5-pro-exp-03-25"),
    # model=LiteLlm(model="vertex_ai/gemini-2.5-pro-exp-03-25"),
    # model=LiteLlm(model="vertex_ai/claude-3-5-haiku"),
    model=LiteLlm(model="openai/gpt-4o"),
    # model=LiteLlm(model="anthropic/claude-3-sonnet-20240229"),
    name="data_processing_agent",
    description=(
        "hello world agent that can roll a dice of 8 sides and check prime"
        " numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
import agent
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  session_service = InMemorySessionService()
  artifact_service = InMemoryArtifactService()
  runner = Runner(
      app_name=app_name,
      agent=agent.root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  session_11 = await session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi, introduce yourself.')
  await run_prompt(
      session_11, 'Roll a die with 100 sides and check if it is prime'
  )
  await run_prompt(session_11, 'Roll it again.')
  await run_prompt(session_11, 'What numbers did I got?')
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk.agents import Agent
from google.adk.tools.example_tool import ExampleTool
from google.genai import types
# --- Roll Die Sub-Agent ---
def roll_die(sides: int) -> int:
  """Roll a die and return the rolled result."""
  return random.randint(1, sides)
roll_agent = Agent(
    name="roll_agent",
    description="Handles rolling dice of different sizes.",
    instruction="""
      You are responsible for rolling dice based on the user's request.
      When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
    """,
    tools=[roll_die],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
# --- Prime Check Sub-Agent ---
def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime."""
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      "No prime numbers found."
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
example_tool = ExampleTool([
    {
        "input": {
            "role": "user",
            "parts": [{"text": "Roll a 6-sided die."}],
        },
        "output": [
            {"role": "model", "parts": [{"text": "I rolled a 4 for you."}]}
        ],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "Is 7 a prime number?"}],
        },
        "output": [{
            "role": "model",
            "parts": [{"text": "Yes, 7 is a prime number."}],
        }],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "Roll a 10-sided die and check if it's prime."}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "I rolled an 8 for you."}],
            },
            {
                "role": "model",
                "parts": [{"text": "8 is not a prime number."}],
            },
        ],
    },
])
prime_agent = Agent(
    name="prime_agent",
    description="Handles checking if numbers are prime.",
    instruction="""
      You are responsible for checking whether numbers are prime.
      When asked to check primes, you must call the check_prime tool with a list of integers.
      Never attempt to determine prime numbers manually.
      Return the prime number results to the root agent.
    """,
    tools=[check_prime],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
root_agent = Agent(
    model="gemini-1.5-flash",
    name="root_agent",
    instruction="""
      You are a helpful assistant that can roll dice and check if numbers are prime.
      You delegate rolling dice tasks to the roll_agent and prime checking tasks to the prime_agent.
      Follow these steps:
      1. If the user asks to roll a die, delegate to the roll_agent.
      2. If the user asks to check primes, delegate to the prime_agent.
      3. If the user asks to roll a die and then check if the result is prime, call roll_agent first, then pass the result to prime_agent.
      Always clarify the results before proceeding.
    """,
    global_instruction=(
        "You are DicePrimeBot, ready to roll dice and check prime numbers."
    ),
    sub_agents=[roll_agent, prime_agent],
    tools=[example_tool],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
================================================
================================================
# Using ollama models with ADK
## Model choice
If your agent is relying on tools, please make sure that you select a model with tool support from [ollama website](https://ollama.com/search?c=tools).
For reliable results, we recommend using a decent size model with tool support.
The tool support for the model can be checked with the following command:
```bash
ollama show mistral-small3.1
  Model
    architecture        mistral3
    parameters          24.0B
    context length      131072
    embedding length    5120
    quantization        Q4_K_M
  Capabilities
    completion
    vision
    tools
```
You are supposed to see `tools` listed under capabilities.
You can also look at the template the model is using and tweak it based on your needs.
```bash
ollama show --modelfile llama3.1 > model_file_to_modify
```
Then you can create a model with the following command:
```bash
ollama create llama3.1-modified -f model_file_to_modify
```
## Using ollama_chat provider
Our LiteLlm wrapper can be used to create agents with ollama models.
```py
root_agent = Agent(
    model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    name="dice_agent",
    description=(
        "hello world agent that can roll a dice of 8 sides and check prime"
        " numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
)
```
**It is important to set the provider `ollama_chat` instead of `ollama`. Using `ollama` will result in unexpected behaviors such as infinite tool call loops and ignoring previous context.**
While `api_base` can be provided inside litellm for generation, litellm library is calling other APIs relying on the env variable instead as of v1.65.5 after completion. So at this time, we recommend setting the env variable `OLLAMA_API_BASE` to point to the ollama server.
```bash
export OLLAMA_API_BASE="http://localhost:11434"
adk web
```
## Using openai provider
Alternatively, `openai` can be used as the provider name. But this will also require setting the  `OPENAI_API_BASE=http://localhost:11434/v1` and `OPENAI_API_KEY=anything` env variables instead of `OLLAMA_API_BASE`. **Please notice that api base now has `/v1` at the end.**
```py
root_agent = Agent(
    model=LiteLlm(model="openai/mistral-small3.1"),
    name="dice_agent",
    description=(
        "hello world agent that can roll a dice of 8 sides and check prime"
        " numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
)
```
```bash
export OPENAI_API_BASE=http://localhost:11434/v1
export OPENAI_API_KEY=anything
adk web
```
## Debugging
You can see the request sent to the ollama server by adding the following in your agent code just after imports.
```py
import litellm
litellm._turn_on_debug()
```
Look for a line like the following:
```bash
quest Sent from LiteLLM:
curl -X POST \
http://localhost:11434/api/chat \
-d '{'model': 'mistral-small3.1', 'messages': [{'role': 'system', 'content': ...
```
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
def roll_die(sides: int) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  return random.randint(1, sides)
def check_prime(numbers: list[int]) -> str:
  """Check if a given list of numbers are prime.
  Args:
    numbers: The list of numbers to check.
  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in numbers:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      "No prime numbers found."
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
root_agent = Agent(
    model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    name="dice_roll_agent",
    description=(
        "hello world agent that can roll a dice of any number of sides and"
        " check prime numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
import warnings
import agent
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
warnings.filterwarnings('ignore', category=UserWarning)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  session_service = InMemorySessionService()
  artifact_service = InMemoryArtifactService()
  runner = Runner(
      app_name=app_name,
      agent=agent.root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  session_11 = await session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi, introduce yourself.')
  await run_prompt(
      session_11, 'Roll a die with 100 sides and check if it is prime'
  )
  await run_prompt(session_11, 'Roll it again.')
  await run_prompt(session_11, 'What numbers did I get?')
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
# Agent with Long-Running Tools
This example demonstrates an agent using a long-running tool (`ask_for_approval`).
## Key Flow for Long-Running Tools
1.  **Initial Call**: The agent calls the long-running tool (e.g., `ask_for_approval`).
2.  **Initial Tool Response**: The tool immediately returns an initial response, typically indicating a "pending" status and a way to track the request (e.g., a `ticket-id`). This is sent back to the agent as a `types.FunctionResponse` (usually processed internally by the runner and then influencing the agent's next turn).
3.  **Agent Acknowledges**: The agent processes this initial response and usually informs the user about the pending status.
4.  **External Process/Update**: The long-running task progresses externally (e.g., a human approves the request).
5.  **❗️Crucial Step: Provide Updated Tool Response❗️**:
    * Once the external process completes or updates, your application **must** construct a new `types.FunctionResponse`.
    * This response should use the **same `id` and `name`** as the original `FunctionCall` to the long-running tool.
    * The `response` field within this `types.FunctionResponse` should contain the *updated data* (e.g., `{'status': 'approved', ...}`).
    * Send this `types.FunctionResponse` back to the agent as a part within a new message using `role="user"`.
    ```python
    # Example: After external approval
    updated_tool_output_data = {
        "status": "approved",
        "ticket-id": ticket_id, # from original call
        # ... other relevant updated data
    }
    updated_function_response_part = types.Part(
        function_response=types.FunctionResponse(
            id=long_running_function_call.id,   # Original call ID
            name=long_running_function_call.name, # Original call name
            response=updated_tool_output_data,
        )
    )
    # Send this back to the agent
    await runner.run_async(
        # ... session_id, user_id ...
        new_message=types.Content(
            parts=[updated_function_response_part], role="user"
        ),
    )
    ```
6.  **Agent Acts on Update**: The agent receives this message containing the `types.FunctionResponse` and, based on its instructions, proceeds with the next steps (e.g., calling another tool like `reimburse`).
**Why is this important?** The agent relies on receiving this subsequent `types.FunctionResponse` (provided in a message with `role="user"` containing the specific `Part`) to understand that the long-running task has concluded or its state has changed. Without it, the agent will remain unaware of the outcome of the pending task.
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from google.adk import Agent
from google.adk.tools import ToolContext
from google.adk.tools.long_running_tool import LongRunningFunctionTool
from google.genai import types
def reimburse(purpose: str, amount: float) -> str:
  """Reimburse the amount of money to the employee."""
  return {
      'status': 'ok',
  }
def ask_for_approval(
    purpose: str, amount: float, tool_context: ToolContext
) -> dict[str, Any]:
  """Ask for approval for the reimbursement."""
  return {
      'status': 'pending',
      'amount': amount,
      'ticketId': 'reimbursement-ticket-001',
  }
root_agent = Agent(
    model='gemini-1.5-flash',
    name='reimbursement_agent',
    instruction="""
      You are an agent whose job is to handle the reimbursement process for
      the employees. If the amount is less than $100, you will automatically
      approve the reimbursement.
      If the amount is greater than $100, you will
      ask for approval from the manager. If the manager approves, you will
      call reimburse() to reimburse the amount to the employee. If the manager
      rejects, you will inform the employee of the rejection.
""",
    tools=[reimburse, LongRunningFunctionTool(func=ask_for_approval)],
    generate_content_config=types.GenerateContentConfig(temperature=0.1),
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import agent
from dotenv import load_dotenv
from typing import Any
from typing import Union
from google.adk.agents import Agent
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.tools import LongRunningFunctionTool
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import export
from opentelemetry.sdk.trace import TracerProvider
load_dotenv(override=True)
APP_NAME = "human_in_the_loop"
USER_ID = "1234"
SESSION_ID = "session1234"
session_service = InMemorySessionService()
async def main():
  session = await session_service.create_session(
      app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
  )
  runner = Runner(
      agent=agent.root_agent,
      app_name=APP_NAME,
      session_service=session_service,
  )
  async def call_agent(query: str):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f'>>> User Query: "{query}"')
    print("--- Running agent's initial turn ---")
    events_async = runner.run_async(
        session_id=session.id, user_id=USER_ID, new_message=content
    )
    long_running_function_call: Union[types.FunctionCall, None] = None
    initial_tool_response: Union[types.FunctionResponse, None] = None
    ticket_id: Union[str, None] = None
    async for event in events_async:
      if event.content and event.content.parts:
        for i, part in enumerate(event.content.parts):
          if part.text:
            print(f"    Part {i} [Text]: {part.text.strip()}")
          if part.function_call:
            print(
                f"    Part {i} [FunctionCall]:"
                f" {part.function_call.name}({part.function_call.args}) ID:"
                f" {part.function_call.id}"
            )
            if not long_running_function_call and part.function_call.id in (
                event.long_running_tool_ids or []
            ):
              long_running_function_call = part.function_call
              print(
                  "      (Captured as long_running_function_call for"
                  f" '{part.function_call.name}')"
              )
          if part.function_response:
            print(
                f"    Part {i} [FunctionResponse]: For"
                f" '{part.function_response.name}', ID:"
                f" {part.function_response.id}, Response:"
                f" {part.function_response.response}"
            )
            if (
                long_running_function_call
                and part.function_response.id == long_running_function_call.id
            ):
              initial_tool_response = part.function_response
              if initial_tool_response.response:
                ticket_id = initial_tool_response.response.get("ticketId")
              print(
                  "      (Captured as initial_tool_response for"
                  f" '{part.function_response.name}', Ticket ID: {ticket_id})"
              )
    print("--- End of agent's initial turn ---\n")
    if (
        long_running_function_call
        and initial_tool_response
        and initial_tool_response.response.get("status") == "pending"
    ):
      print(f"--- Simulating external approval for ticket: {ticket_id} ---\n")
      updated_tool_output_data = {
          "status": "approved",
          "ticketId": ticket_id,
          "approver_feedback": "Approved by manager at " + str(
              asyncio.get_event_loop().time()
          ),
      }
      updated_function_response_part = types.Part(
          function_response=types.FunctionResponse(
              id=long_running_function_call.id,
              name=long_running_function_call.name,
              response=updated_tool_output_data,
          )
      )
      print(
          "--- Sending updated tool result to agent for call ID"
          f" {long_running_function_call.id}: {updated_tool_output_data} ---"
      )
      print("--- Running agent's turn AFTER receiving updated tool result ---")
      async for event in runner.run_async(
          session_id=session.id,
          user_id=USER_ID,
          new_message=types.Content(
              parts=[updated_function_response_part], role="user"
          ),
      ):
        if event.content and event.content.parts:
          for i, part in enumerate(event.content.parts):
            if part.text:
              print(f"    Part {i} [Text]: {part.text.strip()}")
            if part.function_call:
              print(
                  f"    Part {i} [FunctionCall]:"
                  f" {part.function_call.name}({part.function_call.args}) ID:"
                  f" {part.function_call.id}"
              )
            if part.function_response:
              print(
                  f"    Part {i} [FunctionResponse]: For"
                  f" '{part.function_response.name}', ID:"
                  f" {part.function_response.id}, Response:"
                  f" {part.function_response.response}"
              )
      print("--- End of agent's turn AFTER receiving updated tool result ---")
    elif long_running_function_call and not initial_tool_response:
      print(
          f"--- Long running function '{long_running_function_call.name}' was"
          " called, but its initial response was not captured. ---"
      )
    elif not long_running_function_call:
      print(
          "--- No long running function call was detected in the initial"
          " turn. ---"
      )
  await call_agent("Please reimburse $50 for meals")
  print("=" * 70)
  await call_agent("Please reimburse $200 for conference travel")
if __name__ == "__main__":
  provider = TracerProvider()
  if not project_id:
  print("Tracing to project", project_id)
  processor = export.BatchSpanProcessor(
      CloudTraceSpanExporter(project_id=project_id)
  )
  provider.add_span_processor(processor)
  trace.set_tracer_provider(provider)
  asyncio.run(main())
  provider.force_flush()
  print("Done tracing to project", project_id)
================================================
================================================
# Application Integration Agent Sample with End-User Credentials
## Introduction
This sample demonstrates how to use the `ApplicationIntegrationToolset` within
an ADK agent to interact with external applications using **end-user OAuth 2.0
credentials**. Specifically, this agent (`agent.py`) is configured to interact
with Google Calendar using a pre-configured Application Integration connection
and authenticating as the end user.
## Prerequisites
1.  **Set up Integration Connection:**
    *   You need an existing
        [Integration connection](https://cloud.google.com/integration-connectors/docs/overview)
        configured to interact with Google Calendar APIs. Follow the
        to provision the Integration Connector in Google Cloud. You will need
        the `Connection Name`, `Project ID`, and `Location` of your connection.
    *   Ensure the connection is configured to use Google Calendar (e.g., by
        enabling the `google-calendar-connector` or a similar connector).
2.  **Configure OAuth 2.0 Client:**
    *   You need an OAuth 2.0 Client ID and Client Secret that is authorized to
        access the required Google Calendar scopes (e.g.,
        `https://www.googleapis.com/auth/calendar.readonly`). You can create
        OAuth credentials in the Google Cloud Console under "APIs & Services"
        -> "Credentials".
3.  **Configure Environment Variables:**
    *   Create a `.env` file in the same directory as `agent.py` (or add to
        your existing one).
    *   Add the following variables to the `.env` file, replacing the
        placeholder values with your actual connection details:
      ```dotenv
      CONNECTION_NAME=<YOUR_CALENDAR_CONNECTION_NAME>
      CONNECTION_LOCATION=<YOUR_CONNECTION_LOCATION>
      CLIENT_ID=<YOUR_OAUTH_CLIENT_ID>
      CLIENT_SECRET=<YOUR_OAUTH_CLIENT_SECRET>
      ```
## End-User Authentication (OAuth 2.0)
This agent utilizes the `AuthCredential` and `OAuth2Auth` classes from the ADK
to handle authentication.
*   It defines an OAuth 2.0 scheme (`oauth2_scheme`) based on Google Cloud's
    OAuth endpoints and required scopes.
*   It uses the `CLIENT_ID` and `CLIENT_SECRET` from the environment variables
    (or hardcoded values in the sample) to configure `OAuth2Auth`.
*   This `AuthCredential` is passed to the `ApplicationIntegrationToolset`,
    enabling the tool to make authenticated API calls to Google Calendar on
    behalf of the user running the agent. The ADK framework will typically
    handle the OAuth flow (e.g., prompting the user for consent) when the tool
    is first invoked.
## How to Use
1.  **Install Dependencies:** Ensure you have the necessary libraries installed
    (e.g., `google-adk`, `python-dotenv`).
2.  **Run the Agent:** Execute the agent script from your terminal:
    ```bash
    python agent.py
    ```
3.  **Interact:** Once the agent starts, you can interact with it. If it's the
    first time using the tool requiring OAuth, you might be prompted to go
    through the OAuth consent flow in your browser. After successful
    authentication, you can ask the agent to perform tasks.
## Sample Prompts
Here are some examples of how you can interact with the agent:
*   `Can you list events from my primary calendar?`
================================================
================================================
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import dict_to_auth_scheme
from google.genai import types
# Load environment variables from .env file
load_dotenv()
connection_name = os.getenv("CONNECTION_NAME")
connection_location = os.getenv("CONNECTION_LOCATION")
client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")
oauth2_data_google_cloud = {
    "type": "oauth2",
    "flows": {
        "authorizationCode": {
            "authorizationUrl": "https://accounts.google.com/o/oauth2/auth",
            "tokenUrl": "https://oauth2.googleapis.com/token",
            "scopes": {
                "https://www.googleapis.com/auth/cloud-platform": (
                    "View and manage your data across Google Cloud Platform"
                    " services"
                ),
                "https://www.googleapis.com/auth/calendar.readonly": (
                    "View your calendars"
                ),
            },
        }
    },
}
oauth2_scheme = dict_to_auth_scheme(oauth2_data_google_cloud)
auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id=client_id,
        client_secret=client_secret,
    ),
)
calendar_tool = ApplicationIntegrationToolset(
    project=connection_project,
    location=connection_location,
    tool_name_prefix="calendar_tool",
    connection=connection_name,
    actions=["GET_calendars/%7BcalendarId%7D/events"],
    tool_instructions="""
  Use this tool to list events in a calendar. Get calendarId from the user and use it in tool as following example:
  connectorInputPayload: { "Path parameters": { "calendarId": "primary" } }. Follow the schema correctly. Note its "Path parameters" and not "Path_parameters".
    """,
    auth_scheme=oauth2_scheme,
    auth_credential=auth_credential,
)
root_agent = Agent(
    model="gemini-2.0-flash",
    name="data_processing_agent",
    description="Agent that can list events in a calendar.",
    instruction="""
      Helps you with calendar related tasks.
    """,
    tools=calendar_tool.get_tools(),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
================================================
================================================
**Instructions to connect to an agent:**
**Use Integration Connectors**
Connect your agent to enterprise applications using [Integration Connectors](https://cloud.google.com/integration-connectors/docs/overview).
**Steps:**
1. To use a connector from Integration Connectors, you need to [provision](https://console.cloud.google.com/) Application Integration in the same region as your connection by clicking on "QUICK SETUP" button.
Google Cloud Tools
2. Go to [Connection Tool]((https://console.cloud.google.com/)) template from the template library and click on "USE TEMPLATE" button.
3. Fill the Integration Name as **ExecuteConnection** (It is mandatory to use this integration name only) and select the region same as the connection region. Click on "CREATE".
4. Publish the integration by using the "PUBLISH" button on the Application Integration Editor.
**References:**
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.agents import Agent
from .tools import jira_tool
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='jira_connector_agent',
    description="This agent helps search issues in JIRA",
    instruction="""
        To start with, greet the user
        First, you will be given a description of what you can do.
        You the jira agent, who can help the user by fetching the jira issues based on the user query inputs
        If an User wants to display all issues, then output only Key, Description, Summary, Status fields in a **clear table format** with key information. Example given below. Separate each line. 
        If an User wants to fetch on one specific key then use the LIST operation to fetch all Jira issues. Then filter locally to display only filtered result as per User given key input.
          - **User query:** "give me the details of SMP-2"
          - Output only Key, Description, Summary, Status fields in a **clear table format** with key information.
        Example scenarios:
        - **User query:** "Can you show me all Jira issues with status `Done`?"
        - **User query:** "can you give details of SMP-2?"
        - **User query:** "Show issues with summary containing 'World'"
        - **User query:** "Show issues with description containing 'This is example task 3'"
        **Important Notes:**
        - I currently support only **GET** and **LIST** operations.
    """,
    tools=jira_tool.get_tools(),
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
jira_tool = ApplicationIntegrationToolset(
    project="your-gcp-project-id",  # replace with your GCP project ID
    location="your-regions",  # replace your regions
    connection="your-integration-connection-name", #replace with your connection name
    entity_operations={
        "Issues": ["GET", "LIST"],
    },
    actions=[
        "get_issue_by_key",
    ],
    tool_name="jira_conversation_tool",
    tool_instructions="""
    This tool is to call an integration to search for issues in JIRA
    """,
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
"""
from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_core.tools.structured import StructuredTool
from pydantic import BaseModel
def add(x, y) -> int:
  return x + y
class AddSchema(BaseModel):
  x: int
  y: int
    add,
    name="add",
    description="Adds two numbers",
    args_schema=AddSchema,
)
root_agent = Agent(
    model="gemini-2.0-flash-001",
    description="A helpful assistant for user questions.",
    instruction=(
        "You are a helpful assistant for user questions, you have access to a"
        " tool that adds two numbers."
    ),
)
================================================
================================================
# Langchain Youtube Search Agent
This agent utilize the Lanchain YoutubeSearchTool to search youtubes.
You need to install below dependencies:
```python
``` 
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.agents import LlmAgent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import YouTubeSearchTool
# Instantiate the tool
langchain_yt_tool = YouTubeSearchTool()
# Wrap the tool in the LangchainTool class from ADK
adk_yt_tool = LangchainTool(
    tool=langchain_yt_tool,
)
root_agent = LlmAgent(
    name="youtube_search_agent",
    model="gemini-2.0-flash",  # Replace with the actual model name
    instruction="""
    Ask customer to provide singer name, and the number of videos to search.
    """,
    description="Help customer to search for a video on Youtube.",
    tools=[adk_yt_tool],
    output_key="youtube_search_output",
)
================================================
================================================
youtube_search
================================================
================================================
This agent connects to a local MCP server via sse.
To run this agent, start the local MCP server first by :
```bash
```
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseServerParams
_allowed_path = os.path.dirname(os.path.abspath(__file__))
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction=f"""\
Help user accessing their file systems.
Allowed directory: {_allowed_path}
    """,
    tools=[
        MCPToolset(
            connection_params=SseServerParams(
                url='http://localhost:3000/sse',
                headers={'Accept': 'text/event-stream'},
            ),
            # don't want agent to do write operation
            # you can also do below
            # tool_filter=lambda tool, ctx=None: tool.name
            # not in [
            #     'write_file',
            #     'edit_file',
            #     'create_directory',
            #     'move_file',
            # ],
            tool_filter=[
                'read_file',
                'read_multiple_files',
                'list_directory',
                'directory_tree',
                'search_files',
                'get_file_info',
                'list_allowed_directories',
            ],
        )
    ],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import os
from pathlib import Path
import sys
from mcp.server.fastmcp import FastMCP
# Create an MCP server with a name
mcp = FastMCP("Filesystem Server", host="localhost", port=3000)
# Add a tool to read file contents
@mcp.tool(description="Read contents of a file")
def read_file(filepath: str) -> str:
  """Read and return the contents of a file."""
  with open(filepath, "r") as f:
    return f.read()
# Add a tool to list directory contents
@mcp.tool(description="List contents of a directory")
def list_directory(dirpath: str) -> list:
  """List all files and directories in the given directory."""
  return os.listdir(dirpath)
# Add a tool to get current working directory
@mcp.tool(description="Get current working directory")
def get_cwd() -> str:
  """Return the current working directory."""
  return str(Path.cwd())
# Graceful shutdown handler
async def shutdown(signal, loop):
  """Cleanup tasks tied to the service's shutdown."""
  print(f"\nReceived exit signal {signal.name}...")
  # Get all running tasks
  tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
  # Cancel all tasks
  for task in tasks:
    task.cancel()
  print(f"Cancelling {len(tasks)} outstanding tasks")
  await asyncio.gather(*tasks, return_exceptions=True)
  # Stop the loop
  loop.stop()
  print("Shutdown complete!")
# Main entry point with graceful shutdown handling
if __name__ == "__main__":
  try:
    # The MCP run function ultimately uses asyncio.run() internally
    mcp.run(transport="sse")
  except KeyboardInterrupt:
    print("\nServer shutting down gracefully...")
    # The asyncio event loop has already been stopped by the KeyboardInterrupt
    print("Server has been shut down.")
  except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
  finally:
    print("Thank you for using the Filesystem MCP Server!")
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters
_allowed_path = os.path.dirname(os.path.abspath(__file__))
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction=f"""\
Help user accessing their file systems.
Allowed directory: {_allowed_path}
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    '-y',  # Arguments for the command
                    '@modelcontextprotocol/server-filesystem',
                    _allowed_path,
                ],
            ),
            # don't want agent to do write operation
            # you can also do below
            # tool_filter=lambda tool, ctx=None: tool.name
            # not in [
            #     'write_file',
            #     'edit_file',
            #     'create_directory',
            #     'move_file',
            # ],
            tool_filter=[
                'read_file',
                'read_multiple_files',
                'list_directory',
                'directory_tree',
                'search_files',
                'get_file_info',
                'list_allowed_directories',
            ],
        )
    ],
)
================================================
================================================
This agent connects to a local MCP server via sse.
To run this agent, start the local MCP server first by :
```bash
```
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseServerParams
_allowed_path = os.path.dirname(os.path.abspath(__file__))
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction=f"""\
Help user accessing their file systems.
Allowed directory: {_allowed_path}
    """,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:3000/mcp',
            ),
            # don't want agent to do write operation
            # you can also do below
            # tool_filter=lambda tool, ctx=None: tool.name
            # not in [
            #     'write_file',
            #     'edit_file',
            #     'create_directory',
            #     'move_file',
            # ],
            tool_filter=[
                'read_file',
                'read_multiple_files',
                'list_directory',
                'directory_tree',
                'search_files',
                'get_file_info',
                'list_allowed_directories',
            ],
        )
    ],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import os
from pathlib import Path
import sys
from mcp.server.fastmcp import FastMCP
# Create an MCP server with a name
mcp = FastMCP("Filesystem Server", host="localhost", port=3000)
# Add a tool to read file contents
@mcp.tool(description="Read contents of a file")
def read_file(filepath: str) -> str:
  """Read and return the contents of a file."""
  with open(filepath, "r") as f:
    return f.read()
# Add a tool to list directory contents
@mcp.tool(description="List contents of a directory")
def list_directory(dirpath: str) -> list:
  """List all files and directories in the given directory."""
  return os.listdir(dirpath)
# Add a tool to get current working directory
@mcp.tool(description="Get current working directory")
def get_cwd() -> str:
  """Return the current working directory."""
  return str(Path.cwd())
# Graceful shutdown handler
async def shutdown(signal, loop):
  """Cleanup tasks tied to the service's shutdown."""
  print(f"\nReceived exit signal {signal.name}...")
  # Get all running tasks
  tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
  # Cancel all tasks
  for task in tasks:
    task.cancel()
  print(f"Cancelling {len(tasks)} outstanding tasks")
  await asyncio.gather(*tasks, return_exceptions=True)
  # Stop the loop
  loop.stop()
  print("Shutdown complete!")
# Main entry point with graceful shutdown handling
if __name__ == "__main__":
  try:
    # The MCP run function ultimately uses asyncio.run() internally
    mcp.run(transport="streamable-http")
  except KeyboardInterrupt:
    print("\nServer shutting down gracefully...")
    # The asyncio event loop has already been stopped by the KeyboardInterrupt
    print("Server has been shut down.")
  except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
  finally:
    print("Thank you for using the Filesystem MCP Server!")
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from google.adk import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.load_memory_tool import load_memory_tool
from google.adk.tools.preload_memory_tool import preload_memory_tool
def update_current_time(callback_context: CallbackContext):
  callback_context.state['_time'] = datetime.now().isoformat()
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='memory_agent',
    description='agent that have access to memory tools.',
    before_agent_callback=update_current_time,
    instruction="""\
You are an agent that help user answer questions.
Current time: {_time}
""",
    tools=[
        load_memory_tool,
        preload_memory_tool,
    ],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from datetime import datetime
from datetime import timedelta
from typing import cast
import agent
from dotenv import load_dotenv
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  runner = InMemoryRunner(
      app_name=app_name,
      agent=agent.root_agent,
  )
  async def run_prompt(session: Session, new_message: str) -> Session:
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if not event.content or not event.content.parts:
        continue
      if event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
      elif event.content.parts[0].function_call:
        print(
            f'** {event.author}: fc /'
            f' {event.content.parts[0].function_call.name} /'
            f' {event.content.parts[0].function_call.args}\n'
        )
      elif event.content.parts[0].function_response:
        print(
            f'** {event.author}: fr /'
            f' {event.content.parts[0].function_response.name} /'
            f' {event.content.parts[0].function_response.response}\n'
        )
    return cast(
        Session,
        await runner.session_service.get_session(
            app_name=app_name, user_id=user_id_1, session_id=session.id
        ),
    )
  session_1 = await runner.session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  print(f'----Session to create memory: {session_1.id} ----------------------')
  session_1 = await run_prompt(session_1, 'Hi')
  session_1 = await run_prompt(session_1, 'My name is Jack')
  session_1 = await run_prompt(session_1, 'I like badminton.')
  session_1 = await run_prompt(
      session_1,
      f'I ate a burger on {(datetime.now() - timedelta(days=1)).date()}.',
  )
  session_1 = await run_prompt(
      session_1,
      f'I ate a banana on {(datetime.now() - timedelta(days=2)).date()}.',
  )
  print('Saving session to memory service...')
  if runner.memory_service:
    await runner.memory_service.add_session_to_memory(session_1)
  print('-------------------------------------------------------------------')
  session_2 = await runner.session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  print(f'----Session to use memory: {session_2.id} ----------------------')
  session_2 = await run_prompt(session_2, 'Hi')
  session_2 = await run_prompt(session_2, 'What do I like to do?')
  # ** memory_agent: You like badminton.
  session_2 = await run_prompt(session_2, 'When did I say that?')
  # ** memory_agent: You said you liked badminton on ...
  session_2 = await run_prompt(session_2, 'What did I eat yesterday?')
  # ** memory_agent: You ate a burger yesterday...
  print('-------------------------------------------------------------------')
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.agents import Agent
from google.adk.agents import SequentialAgent
sub_agent_1 = Agent(
    name='sub_agent_1',
    description='No.1 sub agent.',
    model='gemini-2.0-flash-001',
    instruction='JUST SAY 1.',
)
sub_agent_2 = Agent(
    name='sub_agent_2',
    description='No.2 sub agent.',
    model='gemini-2.0-flash-001',
    instruction='JUST SAY 2.',
)
sequential_agent = SequentialAgent(
    name='sequential_agent',
    sub_agents=[sub_agent_1, sub_agent_2],
)
root_agent = sequential_agent
================================================
================================================
# OAuth Sample
## Introduction
* 1. list_calendar_events
  This is a customized tool that calls Google Calendar API to list calendar events.
  It pass in the client id and client secrete to ADK and then get back the access token from ADK.
  And then it uses the access token to call calendar api.
* 2. get_calendar_events
  This is an google calendar tool that calls Google Calendar API to get the details of a specific calendar.
  This tool is from the ADK built-in Google Calendar ToolSet.
  Everything is wrapped and the tool user just needs to pass in the client id and client secret.
## How to use
* 1. Follow https://developers.google.com/identity/protocols/oauth2#1.-obtain-oauth-2.0-credentials-from-the-dynamic_data.setvar.console_name. to get your client id and client secret.
  Be sure to choose "web" as your client type.
* 2. Configure your `.env` file to add two variables:
  * OAUTH_CLIENT_ID={your client id}
  * OAUTH_CLIENT_SECRET={your client secret}
  Note: don't create a separate `.env` file , instead put it to the same `.env` file that stores your Vertex AI or Dev ML credentials
* 3. Follow https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred to add http://localhost/dev-ui/ to "Authorized redirect URIs".
  Note: localhost here is just a hostname that you use to access the dev ui, replace it with the actual hostname you use to access the dev ui.
* 4. For 1st run, allow popup for localhost in Chrome.
## Sample prompt
* `List all my today's meeting from 7am to 7pm.`
* `Get the details of the first event.`
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows
from google.adk import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.auth import AuthConfig
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth
from google.adk.tools import ToolContext
from google.adk.tools.google_api_tool import CalendarToolset
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
# Load environment variables from .env file
load_dotenv()
# Access the variable
oauth_client_id = os.getenv("OAUTH_CLIENT_ID")
oauth_client_secret = os.getenv("OAUTH_CLIENT_SECRET")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
calendar_toolset = CalendarToolset(
    # you can also replace below customized `list_calendar_events` with build-in
    # google calendar tool by adding `calendar_events_list` in the filter list
    client_id=oauth_client_id,
    client_secret=oauth_client_secret,
    tool_filter=["calendar_events_get"],
)
def list_calendar_events(
    start_time: str,
    end_time: str,
    limit: int,
    tool_context: ToolContext,
) -> list[dict]:
  """Search for calendar events.
  Example:
      flights = get_calendar_events(
          calendar_id='joedoe@gmail.com',
          start_time='2024-09-17T06:00:00',
          end_time='2024-09-17T12:00:00',
          limit=10
      )
      # Returns up to 10 calendar events between 6:00 AM and 12:00 PM on
      September 17, 2024.
  Args:
      calendar_id (str): the calendar ID to search for events.
      start_time (str): The start of the time range (format is
        YYYY-MM-DDTHH:MM:SS).
      end_time (str): The end of the time range (format is YYYY-MM-DDTHH:MM:SS).
      limit (int): The maximum number of results to return.
  Returns:
      list[dict]: A list of events that match the search criteria.
  """
  creds = None
  # Check if the tokes were already in the session state, which means the user
  # has already gone through the OAuth flow and successfully authenticated and
  # authorized the tool to access their calendar.
  if "calendar_tool_tokens" in tool_context.state:
    creds = Credentials.from_authorized_user_info(
        tool_context.state["calendar_tool_tokens"], SCOPES
    )
  if not creds or not creds.valid:
    # If the access token is expired, refresh it with the refresh token.
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      auth_scheme = OAuth2(
          flows=OAuthFlows(
              authorizationCode=OAuthFlowAuthorizationCode(
                  authorizationUrl="https://accounts.google.com/o/oauth2/auth",
                  tokenUrl="https://oauth2.googleapis.com/token",
                  scopes={
                      "https://www.googleapis.com/auth/calendar": (
                          "See, edit, share, and permanently delete all the"
                          " calendars you can access using Google Calendar"
                      )
                  },
              )
          )
      )
      auth_credential = AuthCredential(
          auth_type=AuthCredentialTypes.OAUTH2,
          oauth2=OAuth2Auth(
              client_id=oauth_client_id, client_secret=oauth_client_secret
          ),
      )
      # If the user has not gone through the OAuth flow before, or the refresh
      # token also expired, we need to ask users to go through the OAuth flow.
      # First we check whether the user has just gone through the OAuth flow and
      # Oauth response is just passed back.
      auth_response = tool_context.get_auth_response(
          AuthConfig(
              auth_scheme=auth_scheme, raw_auth_credential=auth_credential
          )
      )
      if auth_response:
        # ADK exchanged the access token already for us
        access_token = auth_response.oauth2.access_token
        refresh_token = auth_response.oauth2.refresh_token
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=auth_scheme.flows.authorizationCode.tokenUrl,
            client_id=oauth_client_id,
            client_secret=oauth_client_secret,
            scopes=list(auth_scheme.flows.authorizationCode.scopes.keys()),
        )
      else:
        # If there are no auth response which means the user has not gone
        # through the OAuth flow yet, we need to ask users to go through the
        # OAuth flow.
        tool_context.request_credential(
            AuthConfig(
                auth_scheme=auth_scheme,
                raw_auth_credential=auth_credential,
            )
        )
        # The return value is optional and could be any dict object. It will be
        # wrapped in a dict with key as 'result' and value as the return value
        # if the object returned is not a dict. This response will be passed
        # to LLM to generate a user friendly message. e.g. LLM will tell user:
        # "I need your authorization to access your calendar. Please authorize
        # me so I can check your meetings for today."
        return "Need User Authorization to access their calendar."
    # We store the access token and refresh token in the session state for the
    # next runs. This is just an example. On production, a tool should store
    # those credentials in some secure store or properly encrypt it before store
    # it in the session state.
    tool_context.state["calendar_tool_tokens"] = json.loads(creds.to_json())
  service = build("calendar", "v3", credentials=creds)
  events_result = (
      service.events()
      .list(
          calendarId="primary",
          timeMin=start_time + "Z" if start_time else None,
          timeMax=end_time + "Z" if end_time else None,
          maxResults=limit,
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])
  return events
def update_time(callback_context: CallbackContext):
  # get current date time
  now = datetime.now()
  formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
  callback_context.state["_time"] = formatted_time
root_agent = Agent(
    model="gemini-2.0-flash",
    name="calendar_agent",
    instruction="""
      You are a helpful personal calendar assistant.
      Use the provided tools to search for calendar events (use 10 as limit if user does't specify), and update them.
      Use "primary" as the calendarId if users don't specify.
      Scenario1:
      The user want to query the calendar events.
      Use list_calendar_events to search for calendar events.
      Scenario2:
      User want to know the details of one of the listed calendar events.
      Use get_calendar_event to get the details of a calendar event.
      Current user:
      <User>
      {userInfo?}
      </User>
      Currnet time: {_time}
""",
    tools=[list_calendar_events, calendar_toolset],
    before_agent_callback=update_time,
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.agents import Agent
def get_weather(city: str) -> dict:
  """Retrieves the current weather report for a specified city.
  Args:
      city (str): The name of the city for which to retrieve the weather report.
  Returns:
      dict: status and result or error msg.
  """
  if city.lower() == "new york":
    return {
        "status": "success",
        "report": (
            "The weather in New York is sunny with a temperature of 25 degrees"
            " Celsius (41 degrees Fahrenheit)."
        ),
    }
  else:
    return {
        "status": "error",
        "error_message": f"Weather information for '{city}' is not available.",
    }
def get_current_time(city: str) -> dict:
  """Returns the current time in a specified city.
  Args:
      city (str): The name of the city for which to retrieve the current time.
  Returns:
      dict: status and result or error msg.
  """
  import datetime
  from zoneinfo import ZoneInfo
  if city.lower() == "new york":
    tz_identifier = "America/New_York"
  else:
    return {
        "status": "error",
        "error_message": (
            f"Sorry, I don't have timezone information for {city}."
        ),
    }
  tz = ZoneInfo(tz_identifier)
  now = datetime.datetime.now(tz)
  report = (
      f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
  )
  return {"status": "success", "report": report}
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "I can answer your questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
================================================
================================================
# Sample Agent to demo session state persistence.
## Lifecycle of session state
After assigning a state using the context object (e.g.
`tool_context.state['log_query_var'] = 'log_query_var_value'`):
* The state is available for use in a later callback.
* Once the resulting event is processed by the runner and appneded in the
  session, the state will be also persisted in the session.
This sample agent is for demonstrating the aforementioned behavior.
## Run the agent
Run below command:
```bash
```
And you should see below output:
```bash
[user]: hello world!
===================== In before_agent_callback ==============================
** Asserting keys are cached in context: ['before_agent_callback_state_key'] pass ✅
** Asserting keys are already persisted in session: [] pass ✅
** Asserting keys are not persisted in session yet: ['before_agent_callback_state_key'] pass ✅
============================================================
===================== In before_model_callback ==============================
** Asserting keys are cached in context: ['before_agent_callback_state_key', 'before_model_callback_state_key'] pass ✅
** Asserting keys are already persisted in session: ['before_agent_callback_state_key'] pass ✅
** Asserting keys are not persisted in session yet: ['before_model_callback_state_key'] pass ✅
============================================================
===================== In after_model_callback ==============================
** Asserting keys are cached in context: ['before_agent_callback_state_key', 'before_model_callback_state_key', 'after_model_callback_state_key'] pass ✅
** Asserting keys are already persisted in session: ['before_agent_callback_state_key'] pass ✅
** Asserting keys are not persisted in session yet: ['before_model_callback_state_key', 'after_model_callback_state_key'] pass ✅
============================================================
[root_agent]: Hello! How can I help you verify something today?
===================== In after_agent_callback ==============================
** Asserting keys are cached in context: ['before_agent_callback_state_key', 'before_model_callback_state_key', 'after_model_callback_state_key', 'after_agent_callback_state_key'] pass ✅
** Asserting keys are already persisted in session: ['before_agent_callback_state_key', 'before_model_callback_state_key', 'after_model_callback_state_key'] pass ✅
** Asserting keys are not persisted in session yet: ['after_agent_callback_state_key'] pass ✅
============================================================
```
## Detailed Explanation
As rule of thumb, to read and write session state, user should assume the
state is available after writing via the context object
(`tool_context`, `callback_context` or `readonly_context`).
### Current Behavior
The current behavior of pesisting states are:
* for `before_agent_callback`: state delta will be persisted after all callbacks are processed.
* for `before_model_callback`: state delta will be persisted with the final LlmResponse,
  aka. after `after_model_callback` is processed.
* for `after_model_callback`: state delta will be persisted together with the event of LlmResponse.
* for `after_agent_callback`: state delta will be persisted after all callbacks are processed.
**NOTE**: the current behavior is considered implementation detail and may be changed later. **DO NOT** rely on it.
================================================
================================================
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""The agent to demo the session state lifecycle.
This agent illustrate how session state will be cached in context and persisted
in session state.
"""
import logging
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
logger = logging.getLogger('google_adk.' + __name__)
async def assert_session_values(
    ctx: CallbackContext,
    title: str,
    *,
    keys_in_ctx_session: Optional[list[str]] = None,
    keys_in_service_session: Optional[list[str]] = None,
    keys_not_in_service_session: Optional[list[str]] = None,
):
  session_in_ctx = ctx._invocation_context.session
  session_in_service = (
      await ctx._invocation_context.session_service.get_session(
          app_name=session_in_ctx.app_name,
          user_id=session_in_ctx.user_id,
          session_id=session_in_ctx.id,
      )
  )
  assert session_in_service is not None
  print(f'===================== {title} ==============================')
  print(
      f'** Asserting keys are cached in context: {keys_in_ctx_session}', end=' '
  )
  for key in keys_in_ctx_session or []:
    assert key in session_in_ctx.state
  print('\033[92mpass ✅\033[0m')
  print(
      '** Asserting keys are already persisted in session:'
      f' {keys_in_service_session}',
      end=' ',
  )
  for key in keys_in_service_session or []:
    assert key in session_in_service.state
  print('\033[92mpass ✅\033[0m')
  print(
      '** Asserting keys are not persisted in session yet:'
      f' {keys_not_in_service_session}',
      end=' ',
  )
  for key in keys_not_in_service_session or []:
    assert key not in session_in_service.state
  print('\033[92mpass ✅\033[0m')
  print('============================================================')
async def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
  if 'before_agent_callback_state_key' in callback_context.state:
    return types.ModelContent('Sorry, I can only reply once.')
  callback_context.state['before_agent_callback_state_key'] = (
      'before_agent_callback_state_value'
  )
  await assert_session_values(
      callback_context,
      'In before_agent_callback',
      keys_in_ctx_session=['before_agent_callback_state_key'],
      keys_in_service_session=[],
      keys_not_in_service_session=['before_agent_callback_state_key'],
  )
async def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
):
  callback_context.state['before_model_callback_state_key'] = (
      'before_model_callback_state_value'
  )
  await assert_session_values(
      callback_context,
      'In before_model_callback',
      keys_in_ctx_session=[
          'before_agent_callback_state_key',
          'before_model_callback_state_key',
      ],
      keys_in_service_session=['before_agent_callback_state_key'],
      keys_not_in_service_session=['before_model_callback_state_key'],
  )
async def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
):
  callback_context.state['after_model_callback_state_key'] = (
      'after_model_callback_state_value'
  )
  await assert_session_values(
      callback_context,
      'In after_model_callback',
      keys_in_ctx_session=[
          'before_agent_callback_state_key',
          'before_model_callback_state_key',
          'after_model_callback_state_key',
      ],
      keys_in_service_session=[
          'before_agent_callback_state_key',
      ],
      keys_not_in_service_session=[
          'before_model_callback_state_key',
          'after_model_callback_state_key',
      ],
  )
async def after_agent_callback(callback_context: CallbackContext):
  callback_context.state['after_agent_callback_state_key'] = (
      'after_agent_callback_state_value'
  )
  await assert_session_values(
      callback_context,
      'In after_agent_callback',
      keys_in_ctx_session=[
          'before_agent_callback_state_key',
          'before_model_callback_state_key',
          'after_model_callback_state_key',
          'after_agent_callback_state_key',
      ],
      keys_in_service_session=[
          'before_agent_callback_state_key',
          'before_model_callback_state_key',
          'after_model_callback_state_key',
      ],
      keys_not_in_service_session=[
          'after_agent_callback_state_key',
      ],
  )
root_agent = Agent(
    name='root_agent',
    description='a verification agent.',
    instruction=(
        'Log all users query with `log_query` tool. Must always remind user you'
        ' cannot answer second query because your setup.'
    ),
    model='gemini-2.0-flash-001',
    before_agent_callback=before_agent_callback,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    after_agent_callback=after_agent_callback,
)
================================================
================================================
{
  "state": {},
  "queries": ["hello world!"]
}
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.genai import types
# --- Roll Die Sub-Agent ---
def roll_die(sides: int) -> int:
  """Roll a die and return the rolled result."""
  return random.randint(1, sides)
roll_agent = LlmAgent(
    name="roll_agent",
    description="Handles rolling dice of different sizes.",
    model="gemini-2.0-flash",
    instruction="""
      You are responsible for rolling dice based on the user's request.
      When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
    """,
    tools=[roll_die],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime."""
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      "No prime numbers found."
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
prime_agent = LlmAgent(
    name="prime_agent",
    description="Handles checking if numbers are prime.",
    model="gemini-2.0-flash",
    instruction="""
      You are responsible for checking whether numbers are prime.
      When asked to check primes, you must call the check_prime tool with a list of integers.
      Never attempt to determine prime numbers manually.
      Return the prime number results to the root agent.
    """,
    tools=[check_prime],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
root_agent = SequentialAgent(
    name="code_pipeline_agent",
    sub_agents=[roll_agent, prime_agent],
    # The agents will run in the order provided: roll_agent -> prime_agent
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
def roll_die(sides: int, tool_context: ToolContext) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  result = random.randint(1, sides)
  if not 'rolls' in tool_context.state:
    tool_context.state['rolls'] = []
  tool_context.state['rolls'] = tool_context.state['rolls'] + [result]
  return result
async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.
  Args:
    nums: The list of numbers to check.
  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )
root_agent = Agent(
    model='gemini-2.0-flash',
    name='data_processing_agent',
    description=(
        'hello world agent that can roll a dice of 8 sides and check prime'
        ' numbers.'
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #     ),
    # ),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import os
import time
import agent
from dotenv import load_dotenv
from google.adk.agents.run_config import RunConfig
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import export
from opentelemetry.sdk.trace import TracerProvider
load_dotenv(override=True)
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  runner = InMemoryRunner(
      agent=agent.root_agent,
      app_name=app_name,
  )
  session_11 = await runner.session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  async def run_prompt_bytes(session: Session, new_message: str):
    content = types.Content(
        role='user',
        parts=[
            types.Part.from_bytes(
                data=str.encode(new_message), mime_type='text/plain'
            )
        ],
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
        run_config=RunConfig(save_input_blobs_as_artifacts=True),
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi')
  await run_prompt(session_11, 'Roll a die with 100 sides')
  await run_prompt(session_11, 'Roll a die again with 100 sides.')
  await run_prompt(session_11, 'What numbers did I got?')
  await run_prompt_bytes(session_11, 'Hi bytes')
  print(
      await runner.artifact_service.list_artifact_keys(
          app_name=app_name, user_id=user_id_1, session_id=session_11.id
      )
  )
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  provider = TracerProvider()
  if not project_id:
  print('Tracing to project', project_id)
  processor = export.BatchSpanProcessor(
      CloudTraceSpanExporter(project_id=project_id)
  )
  provider.add_span_processor(processor)
  trace.set_tracer_provider(provider)
  asyncio.run(main())
  provider.force_flush()
  print('Done tracing to project', project_id)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import random
from google.adk import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.models.anthropic_llm import Claude
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
def roll_die(sides: int, tool_context: ToolContext) -> int:
  """Roll a die and return the rolled result.
  Args:
    sides: The integer number of sides the die has.
  Returns:
    An integer of the result of rolling the die.
  """
  result = random.randint(1, sides)
  if 'rolls' not in tool_context.state:
    tool_context.state['rolls'] = []
  tool_context.state['rolls'] = tool_context.state['rolls'] + [result]
  return result
roll_agent_with_openai = LlmAgent(
    model=LiteLlm(model='openai/gpt-4o'),
    description='Handles rolling dice of different sizes.',
    name='roll_agent_with_openai',
    instruction="""
      You are responsible for rolling dice based on the user's request.
      When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
    """,
    tools=[roll_die],
)
roll_agent_with_claude = LlmAgent(
    model=Claude(model='claude-3-7-sonnet@20250219'),
    description='Handles rolling dice of different sizes.',
    name='roll_agent_with_claude',
    instruction="""
      You are responsible for rolling dice based on the user's request.
      When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
    """,
    tools=[roll_die],
)
roll_agent_with_litellm_claude = LlmAgent(
    model=LiteLlm(model='vertex_ai/claude-3-7-sonnet'),
    description='Handles rolling dice of different sizes.',
    name='roll_agent_with_litellm_claude',
    instruction="""
      You are responsible for rolling dice based on the user's request.
      When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
    """,
    tools=[roll_die],
)
roll_agent_with_gemini = LlmAgent(
    model='gemini-2.0-flash',
    description='Handles rolling dice of different sizes.',
    name='roll_agent_with_gemini',
    instruction="""
      You are responsible for rolling dice based on the user's request.
      When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
    """,
    tools=[roll_die],
)
root_agent = SequentialAgent(
    name='code_pipeline_agent',
    sub_agents=[
        roll_agent_with_openai,
        roll_agent_with_claude,
        roll_agent_with_litellm_claude,
        roll_agent_with_gemini,
    ],
)
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
import warnings
import agent
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.agents.run_config import RunConfig
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
warnings.filterwarnings('ignore', category=UserWarning)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  session_service = InMemorySessionService()
  artifact_service = InMemoryArtifactService()
  runner = Runner(
      app_name=app_name,
      agent=agent.root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  session_11 = await session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  total_prompt_tokens = 0
  total_candidate_tokens = 0
  total_tokens = 0
  async def run_prompt(session: Session, new_message: str):
    nonlocal total_prompt_tokens
    nonlocal total_candidate_tokens
    nonlocal total_tokens
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
      if event.usage_metadata:
        total_prompt_tokens += event.usage_metadata.prompt_token_count or 0
        total_candidate_tokens += (
            event.usage_metadata.candidates_token_count or 0
        )
        total_tokens += event.usage_metadata.total_token_count or 0
        print(
            'Turn tokens:'
            f' {event.usage_metadata.total_token_count} (prompt={event.usage_metadata.prompt_token_count},'
            f' candidates={event.usage_metadata.candidates_token_count})'
        )
    print(
        f'Session tokens: {total_tokens} (prompt={total_prompt_tokens},'
        f' candidates={total_candidate_tokens})'
    )
  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  await run_prompt(session_11, 'Hi')
  await run_prompt(session_11, 'Roll a die with 100 sides')
  print(
      await artifact_service.list_artifact_keys(
          app_name=app_name, user_id=user_id_1, session_id=session_11.id
      )
  )
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
# Toolbox Agent
Follow below steps to run this agent
# Install toolbox
* Run below command:
```bash
export OS="linux/amd64" # one of linux/amd64, darwin/arm64, darwin/amd64, or windows/amd64
curl -O https://storage.googleapis.com/genai-toolbox/v0.5.0/$OS/toolbox
chmod +x toolbox
```
# install SQLite
* install sqlite from https://sqlite.org/
# Create DB (optional. The db instance is already attached in the folder)
* Run below command:
```bash
sqlite3 tool_box.db
```
* Run below SQL:
```sql
CREATE TABLE hotels(
  name          VARCHAR NOT NULL,
  location      VARCHAR NOT NULL,
  price_tier    VARCHAR NOT NULL,
  checkin_date  DATE    NOT NULL,
  checkout_date DATE    NOT NULL,
  booked        BIT     NOT NULL
);
INSERT INTO hotels(id, name, location, price_tier, checkin_date, checkout_date, booked)
VALUES 
  (1, 'Hilton Basel', 'Basel', 'Luxury', '2024-04-22', '2024-04-20', 0),
  (2, 'Marriott Zurich', 'Zurich', 'Upscale', '2024-04-14', '2024-04-21', 0),
  (3, 'Hyatt Regency Basel', 'Basel', 'Upper Upscale', '2024-04-02', '2024-04-20', 0),
  (4, 'Radisson Blu Lucerne', 'Lucerne', 'Midscale', '2024-04-24', '2024-04-05', 0),
  (5, 'Best Western Bern', 'Bern', 'Upper Midscale', '2024-04-23', '2024-04-01', 0),
  (6, 'InterContinental Geneva', 'Geneva', 'Luxury', '2024-04-23', '2024-04-28', 0),
  (7, 'Sheraton Zurich', 'Zurich', 'Upper Upscale', '2024-04-27', '2024-04-02', 0),
  (8, 'Holiday Inn Basel', 'Basel', 'Upper Midscale', '2024-04-24', '2024-04-09', 0),
  (9, 'Courtyard Zurich', 'Zurich', 'Upscale', '2024-04-03', '2024-04-13', 0),
  (10, 'Comfort Inn Bern', 'Bern', 'Midscale', '2024-04-04', '2024-04-16', 0);
```
# create tools configurations
* Create a yaml file named "tools.yaml", see its contents in the agent folder.
# start toolbox server
* Run below commands in the agent folder
```bash
toolbox --tools-file "tools.yaml"
```
# start ADK web UI
# send user query
* query 1: what can you do for me ?
* query 2: could you let know the information about "Hilton Basel" hotel ? 
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.agents import Agent
from google.adk.tools.toolbox_toolset import ToolboxToolset
root_agent = Agent(
    model="gemini-2.0-flash",
    name="root_agent",
    instruction="You are a helpful assistant",
    # Add Toolbox tools to ADK agent
    tools=[
        ToolboxToolset(
            server_url="http://127.0.0.1:5000", toolset_name="my-toolset"
        )
    ],
)
================================================
================================================
[Non-text file]
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
sources:
    my-sqlite-db:
        kind: "sqlite"
        database: "tool_box.db"
tools:
  search-hotels-by-name:
    kind: sqlite-sql
    source: my-sqlite-db
    description: Search for hotels based on name.
    parameters:
      - name: name
        type: string
        description: The name of the hotel.
    statement: SELECT * FROM hotels WHERE name LIKE '%' || $1 || '%';
  search-hotels-by-location:
    kind: sqlite-sql
    source: my-sqlite-db
    description: Search for hotels based on location.
    parameters:
      - name: location
        type: string
        description: The location of the hotel.
    statement: SELECT * FROM hotels WHERE location LIKE '%' || $1 || '%';
  book-hotel:
    kind: sqlite-sql
    source: my-sqlite-db
    description: >-
       Book a hotel by its ID. If the hotel is successfully booked, returns a NULL, raises an error if not.
    parameters:
      - name: hotel_id
        type: string
        description: The ID of the hotel to book.
    statement: UPDATE hotels SET booked = 1 WHERE id = $1;
  update-hotel:
    kind: sqlite-sql
    source: my-sqlite-db
    description: >-
      Update a hotel's check-in and check-out dates by its ID. Returns a message
      indicating  whether the hotel was successfully updated or not.
    parameters:
      - name: hotel_id
        type: string
        description: The ID of the hotel to update.
      - name: checkin_date
        type: string
        description: The new check-in date of the hotel.
      - name: checkout_date
        type: string
        description: The new check-out date of the hotel.
    statement: >-
      UPDATE hotels SET checkin_date = strftime('%Y-%m-%d', replace($2, ',', '')), checkout_date = strftime('%Y-%m-%d', replace($3
      ',', '')) WHERE id = $1;
  cancel-hotel:
    kind: sqlite-sql
    source: my-sqlite-db
    description: Cancel a hotel by its ID.
    parameters:
      - name: hotel_id
        type: string
        description: The ID of the hotel to cancel.
    statement: UPDATE hotels SET booked = 0 WHERE id = $1;
toolsets:
  my-toolset:
    - search-hotels-by-name
    - search-hotels-by-location
    - book-hotel
    - update-hotel
    - cancel-hotel
================================================
================================================
# Workflow Agent Sample - SequentialAgent
Sample query:
* Write a quicksort method in python.
* Write a python function to do bubble sort.
To run in cli (after installing `google-adk`):
Check sample output in `sample.output` file in this folder.
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
# --- 1. Define Sub-Agents for Each Pipeline Stage ---
# Code Writer Agent
# Takes the initial specification (from user query) and writes code.
code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model="gemini-1.5-flash",
    # Change 3: Improved instruction
    instruction="""You are a Python Code Generator.
Based *only* on the user's request, write Python code that fulfills the requirement.
Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```).
Do not add any other text before or after the code block.
""",
    description="Writes initial Python code based on a specification.",
    output_key="generated_code",  # Stores output in state['generated_code']
)
# Code Reviewer Agent
# Takes the code generated by the previous agent (read from state) and provides feedback.
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model="gemini-2.0-flash",
    # Change 3: Improved instruction, correctly using state key injection
    instruction="""You are an expert Python Code Reviewer.
    Your task is to provide constructive feedback on the provided code.
    **Code to Review:**
    ```python
    {generated_code}
    ```
**Review Criteria:**
1.  **Correctness:** Does the code work as intended? Are there logic errors?
2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
5.  **Best Practices:** Does the code follow common Python best practices?
**Output:**
Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
If the code is excellent and requires no changes, simply state: "No major issues found."
Output *only* the review comments or the "No major issues" statement.
""",
    description="Reviews code and provides feedback.",
    output_key="review_comments",  # Stores output in state['review_comments']
)
# Code Refactorer Agent
# Takes the original code and the review comments (read from state) and refactors the code.
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model="gemini-2.0-flash",
    # Change 3: Improved instruction, correctly using state key injection
    instruction="""You are a Python Code Refactoring AI.
Your goal is to improve the given Python code based on the provided review comments.
  **Original Code:**
  ```python
  {generated_code}
  ```
  **Review Comments:**
  {review_comments}
**Task:**
Carefully apply the suggestions from the review comments to refactor the original code.
If the review comments state "No major issues found," return the original code unchanged.
Ensure the final code is complete, functional, and includes necessary imports and docstrings.
**Output:**
Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```).
Do not add any other text before or after the code block.
""",
    description="Refactors code based on review comments.",
    output_key="refactored_code",  # Stores output in state['refactored_code']
)
# --- 2. Create the SequentialAgent ---
# This agent orchestrates the pipeline by running the sub_agents in order.
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent],
    description=(
        "Executes a sequence of code writing, reviewing, and refactoring."
    ),
    # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
)
# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = code_pipeline_agent
================================================
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import cast
import agent
from dotenv import load_dotenv
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
load_dotenv(override=True)
logs.log_to_tmp_folder()
async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  runner = InMemoryRunner(
      app_name=app_name,
      agent=agent.root_agent,
  )
  async def run_prompt(session: Session, new_message: str) -> Session:
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if not event.content or not event.content.parts:
        continue
      if event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
      elif event.content.parts[0].function_call:
        print(
            f'** {event.author}: fc /'
            f' {event.content.parts[0].function_call.name} /'
            f' {event.content.parts[0].function_call.args}\n'
        )
      elif event.content.parts[0].function_response:
        print(
            f'** {event.author}: fr /'
            f' {event.content.parts[0].function_response.name} /'
            f' {event.content.parts[0].function_response.response}\n'
        )
    return cast(
        Session,
        await runner.session_service.get_session(
            app_name=app_name, user_id=user_id_1, session_id=session.id
        ),
    )
  session_1 = await runner.session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )
  print(f'----Session to create memory: {session_1.id} ----------------------')
  session_1 = await run_prompt(
      session_1, 'Write a python function to do quicksort.'
  )
  session_1 = await run_prompt(
      session_1, 'Write another python function to do bubble sort.'
  )
  print('-------------------------------------------------------------------')
if __name__ == '__main__':
  asyncio.run(main())
================================================
================================================
----Session to create memory: a05683c9-4a19-4ba8-b810-e90fc48be566 ----------------------
** User says: {'parts': [{'text': 'Write a python function to do quicksort.'}], 'role': 'user'}
** CodeWriterAgent: ```python
def quicksort(arr):
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less = [i for i in arr[1:] if i <= pivot]
        greater = [i for i in arr[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)
```
** CodeReviewerAgent: *   **Correctness:** The code is functionally correct.
*   **Readability:** The code is fairly readable, utilizing list comprehensions effectively.
*   **Efficiency:** The space complexity is `O(n)` due to the creation of new lists (`less` and `greater`) in each recursive call. Choosing the first element as the pivot can lead to `O(n^2)` time complexity in the worst-case scenario (e.g., a sorted array). A better pivot selection strategy (e.g., random pivot) would improve average performance.
*   **Best Practices:** While the code works, it's not the most efficient implementation of quicksort due to the space complexity and potential for worst-case time complexity. An in-place quicksort algorithm would be more efficient in terms of space.
** CodeRefactorerAgent: ```python
import random
def quicksort(arr):
    """
    Sorts a list using the quicksort algorithm.  This implementation
    uses a randomly selected pivot to improve average-case performance
    and performs the sort in-place to reduce space complexity.
    Args:
        arr (list): The list to be sorted.
    Returns:
        list: The sorted list.
    """
    def _quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            _quicksort(arr, low, pi-1)
            _quicksort(arr, pi+1, high)
    def partition(arr, low, high):
        # Choose a random pivot
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]
        i = (low - 1)
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return (i + 1)
    _quicksort(arr, 0, len(arr)-1)
    return arr
```
** User says: {'parts': [{'text': 'Write another python function to do bubble sort.'}], 'role': 'user'}
** CodeWriterAgent: ```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```
** CodeReviewerAgent: No major issues found.
** CodeRefactorerAgent: ```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```
-------------------------------------------------------------------
================================================
File: src/google/adk/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import version
from .agents.llm_agent import Agent
from .runners import Runner
__version__ = version.__version__
__all__ = ["Agent", "Runner"]
================================================
File: src/google/adk/py.typed
================================================
================================================
File: src/google/adk/runners.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import asyncio
import logging
import queue
import threading
from typing import AsyncGenerator
from typing import Generator
from typing import Optional
import warnings
from google.genai import types
from .agents.active_streaming_tool import ActiveStreamingTool
from .agents.base_agent import BaseAgent
from .agents.invocation_context import InvocationContext
from .agents.invocation_context import new_invocation_context_id
from .agents.live_request_queue import LiveRequestQueue
from .agents.llm_agent import LlmAgent
from .agents.run_config import RunConfig
from .artifacts.base_artifact_service import BaseArtifactService
from .artifacts.in_memory_artifact_service import InMemoryArtifactService
from .code_executors.built_in_code_executor import BuiltInCodeExecutor
from .events.event import Event
from .memory.base_memory_service import BaseMemoryService
from .memory.in_memory_memory_service import InMemoryMemoryService
from .sessions.base_session_service import BaseSessionService
from .sessions.in_memory_session_service import InMemorySessionService
from .sessions.session import Session
from .telemetry import tracer
from .tools.base_toolset import BaseToolset
logger = logging.getLogger('google_adk.' + __name__)
class Runner:
  """The Runner class is used to run agents.
  It manages the execution of an agent within a session, handling message
  processing, event generation, and interaction with various services like
  artifact storage, session management, and memory.
  Attributes:
      app_name: The application name of the runner.
      agent: The root agent to run.
      artifact_service: The artifact service for the runner.
      session_service: The session service for the runner.
      memory_service: The memory service for the runner.
  """
  app_name: str
  """The app name of the runner."""
  agent: BaseAgent
  """The root agent to run."""
  artifact_service: Optional[BaseArtifactService] = None
  """The artifact service for the runner."""
  session_service: BaseSessionService
  """The session service for the runner."""
  memory_service: Optional[BaseMemoryService] = None
  """The memory service for the runner."""
  def __init__(
      self,
      *,
      app_name: str,
      agent: BaseAgent,
      artifact_service: Optional[BaseArtifactService] = None,
      session_service: BaseSessionService,
      memory_service: Optional[BaseMemoryService] = None,
  ):
    """Initializes the Runner.
    Args:
        app_name: The application name of the runner.
        agent: The root agent to run.
        artifact_service: The artifact service for the runner.
        session_service: The session service for the runner.
        memory_service: The memory service for the runner.
    """
    self.app_name = app_name
    self.agent = agent
    self.artifact_service = artifact_service
    self.session_service = session_service
    self.memory_service = memory_service
  def run(
      self,
      *,
      user_id: str,
      session_id: str,
      new_message: types.Content,
      run_config: RunConfig = RunConfig(),
  ) -> Generator[Event, None, None]:
    """Runs the agent.
    Consider using `run_async` for production usage.
    Args:
      user_id: The user ID of the session.
      session_id: The session ID of the session.
      new_message: A new message to append to the session.
      run_config: The run config for the agent.
    Yields:
      The events generated by the agent.
    """
    event_queue = queue.Queue()
    async def _invoke_run_async():
      try:
        async for event in self.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message,
            run_config=run_config,
        ):
          event_queue.put(event)
      finally:
        event_queue.put(None)
    def _asyncio_thread_main():
      try:
        asyncio.run(_invoke_run_async())
      finally:
        event_queue.put(None)
    thread = threading.Thread(target=_asyncio_thread_main)
    thread.start()
    # consumes and re-yield the events from background thread.
    while True:
      event = event_queue.get()
      if event is None:
        break
      else:
        yield event
    thread.join()
  async def run_async(
      self,
      *,
      user_id: str,
      session_id: str,
      new_message: types.Content,
      run_config: RunConfig = RunConfig(),
  ) -> AsyncGenerator[Event, None]:
    """Main entry method to run the agent in this runner.
    Args:
      user_id: The user ID of the session.
      session_id: The session ID of the session.
      new_message: A new message to append to the session.
      run_config: The run config for the agent.
    Yields:
      The events generated by the agent.
    """
    with tracer.start_as_current_span('invocation'):
      session = await self.session_service.get_session(
          app_name=self.app_name, user_id=user_id, session_id=session_id
      )
      if not session:
        raise ValueError(f'Session not found: {session_id}')
      invocation_context = self._new_invocation_context(
          session,
          new_message=new_message,
          run_config=run_config,
      )
      root_agent = self.agent
      if new_message:
        await self._append_new_message_to_session(
            session,
            new_message,
            invocation_context,
            run_config.save_input_blobs_as_artifacts,
        )
      invocation_context.agent = self._find_agent_to_run(session, root_agent)
      async for event in invocation_context.agent.run_async(invocation_context):
        if not event.partial:
          await self.session_service.append_event(session=session, event=event)
        yield event
  async def _append_new_message_to_session(
      self,
      session: Session,
      new_message: types.Content,
      invocation_context: InvocationContext,
      save_input_blobs_as_artifacts: bool = False,
  ):
    """Appends a new message to the session.
    Args:
        session: The session to append the message to.
        new_message: The new message to append.
        invocation_context: The invocation context for the message.
        save_input_blobs_as_artifacts: Whether to save input blobs as artifacts.
    """
    if not new_message.parts:
      raise ValueError('No parts in the new_message.')
    if self.artifact_service and save_input_blobs_as_artifacts:
      # The runner directly saves the artifacts (if applicable) in the
      # user message and replaces the artifact data with a file name
      # placeholder.
      for i, part in enumerate(new_message.parts):
        if part.inline_data is None:
          continue
        file_name = f'artifact_{invocation_context.invocation_id}_{i}'
        await self.artifact_service.save_artifact(
            app_name=self.app_name,
            user_id=session.user_id,
            session_id=session.id,
            filename=file_name,
            artifact=part,
        )
        new_message.parts[i] = types.Part(
            text=f'Uploaded file: {file_name}. It is saved into artifacts'
        )
    # Appends only. We do not yield the event because it's not from the model.
    event = Event(
        invocation_id=invocation_context.invocation_id,
        author='user',
        content=new_message,
    )
    await self.session_service.append_event(session=session, event=event)
  async def run_live(
      self,
      *,
      user_id: Optional[str] = None,
      session_id: Optional[str] = None,
      live_request_queue: LiveRequestQueue,
      run_config: RunConfig = RunConfig(),
      session: Optional[Session] = None,
  ) -> AsyncGenerator[Event, None]:
    """Runs the agent in live mode (experimental feature).
    Args:
        user_id: The user ID for the session. Required if `session` is None.
        session_id: The session ID for the session. Required if `session` is
          None.
        live_request_queue: The queue for live requests.
        run_config: The run config for the agent.
        session: The session to use. This parameter is deprecated, please use
          `user_id` and `session_id` instead.
    Yields:
        AsyncGenerator[Event, None]: An asynchronous generator that yields
        `Event`
        objects as they are produced by the agent during its live execution.
    .. warning::
        This feature is **experimental** and its API or behavior may change
        in future releases.
    .. note::
        Either `session` or both `user_id` and `session_id` must be provided.
    """
    if session is None and (user_id is None or session_id is None):
      raise ValueError(
          'Either session or user_id and session_id must be provided.'
      )
    if session is not None:
      warnings.warn(
          'The `session` parameter is deprecated. Please use `user_id` and'
          ' `session_id` instead.',
          DeprecationWarning,
          stacklevel=2,
      )
    if not session:
      session = await self.session_service.get_session(
          app_name=self.app_name, user_id=user_id, session_id=session_id
      )
      if not session:
        raise ValueError(f'Session not found: {session_id}')
    invocation_context = self._new_invocation_context_for_live(
        session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    root_agent = self.agent
    invocation_context.agent = self._find_agent_to_run(session, root_agent)
    invocation_context.active_streaming_tools = {}
    # TODO(hangfei): switch to use canonical_tools.
    # for shell agents, there is no tools associated with it so we should skip.
    if hasattr(invocation_context.agent, 'tools'):
      for tool in invocation_context.agent.tools:
        # replicate a LiveRequestQueue for streaming tools that relis on
        # LiveRequestQueue
        from typing import get_type_hints
        type_hints = get_type_hints(tool)
        for arg_type in type_hints.values():
          if arg_type is LiveRequestQueue:
            if not invocation_context.active_streaming_tools:
              invocation_context.active_streaming_tools = {}
            active_streaming_tools = ActiveStreamingTool(
                stream=LiveRequestQueue()
            )
            invocation_context.active_streaming_tools[tool.__name__] = (
                active_streaming_tools
            )
    async for event in invocation_context.agent.run_live(invocation_context):
      await self.session_service.append_event(session=session, event=event)
      yield event
  def _find_agent_to_run(
      self, session: Session, root_agent: BaseAgent
  ) -> BaseAgent:
    """Finds the agent to run to continue the session.
    A qualified agent must be either of:
    - The root agent;
    - An LlmAgent who replied last and is capable to transfer to any other agent
      in the agent hierarchy.
    Args:
        session: The session to find the agent for.
        root_agent: The root agent of the runner.
    Returns:
      The agent of the last message in the session or the root agent.
    """
    for event in filter(lambda e: e.author != 'user', reversed(session.events)):
      if event.author == root_agent.name:
        # Found root agent.
        return root_agent
      if not (agent := root_agent.find_sub_agent(event.author)):
        # Agent not found, continue looking.
        logger.warning(
            'Event from an unknown agent: %s, event id: %s',
            event.author,
            event.id,
        )
        continue
      if self._is_transferable_across_agent_tree(agent):
        return agent
    # Falls back to root agent if no suitable agents are found in the session.
    return root_agent
  def _is_transferable_across_agent_tree(self, agent_to_run: BaseAgent) -> bool:
    """Whether the agent to run can transfer to any other agent in the agent tree.
    This typically means all agent_to_run's parent through root agent can
    transfer to their parent_agent.
    Args:
        agent_to_run: The agent to check for transferability.
    Returns:
        True if the agent can transfer, False otherwise.
    """
    agent = agent_to_run
    while agent:
      if not isinstance(agent, LlmAgent):
        # Only LLM-based Agent can provider agent transfer capability.
        return False
      if agent.disallow_transfer_to_parent:
        return False
      agent = agent.parent_agent
    return True
  def _new_invocation_context(
      self,
      session: Session,
      *,
      new_message: Optional[types.Content] = None,
      live_request_queue: Optional[LiveRequestQueue] = None,
      run_config: RunConfig = RunConfig(),
  ) -> InvocationContext:
    """Creates a new invocation context.
    Args:
        session: The session for the context.
        new_message: The new message for the context.
        live_request_queue: The live request queue for the context.
        run_config: The run config for the context.
    Returns:
        The new invocation context.
    """
    invocation_id = new_invocation_context_id()
    if run_config.support_cfc and isinstance(self.agent, LlmAgent):
      model_name = self.agent.canonical_model.model
      if not model_name.startswith('gemini-2'):
        raise ValueError(
            f'CFC is not supported for model: {model_name} in agent:'
            f' {self.agent.name}'
        )
      if not isinstance(self.agent.code_executor, BuiltInCodeExecutor):
        self.agent.code_executor = BuiltInCodeExecutor()
    return InvocationContext(
        artifact_service=self.artifact_service,
        session_service=self.session_service,
        memory_service=self.memory_service,
        invocation_id=invocation_id,
        agent=self.agent,
        session=session,
        user_content=new_message,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
  def _new_invocation_context_for_live(
      self,
      session: Session,
      *,
      live_request_queue: Optional[LiveRequestQueue] = None,
      run_config: RunConfig = RunConfig(),
  ) -> InvocationContext:
    """Creates a new invocation context for live multi-agent."""
    # For live multi-agent, we need model's text transcription as context for
    # next agent.
    if self.agent.sub_agents and live_request_queue:
      if not run_config.response_modalities:
        # default
        run_config.response_modalities = ['AUDIO']
        if not run_config.output_audio_transcription:
          run_config.output_audio_transcription = (
              types.AudioTranscriptionConfig()
          )
      elif 'TEXT' not in run_config.response_modalities:
        if not run_config.output_audio_transcription:
          run_config.output_audio_transcription = (
              types.AudioTranscriptionConfig()
          )
      if not run_config.input_audio_transcription:
        # need this input transcription for agent transferring in live mode.
        run_config.input_audio_transcription = types.AudioTranscriptionConfig()
    return self._new_invocation_context(
        session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
  def _collect_toolset(self, agent: BaseAgent) -> set[BaseToolset]:
    toolsets = set()
    if isinstance(agent, LlmAgent):
      for tool_union in agent.tools:
        if isinstance(tool_union, BaseToolset):
          toolsets.add(tool_union)
    for sub_agent in agent.sub_agents:
      toolsets.update(self._collect_toolset(sub_agent))
    return toolsets
  async def _cleanup_toolsets(self, toolsets_to_close: set[BaseToolset]):
    """Clean up toolsets with proper task context management."""
    if not toolsets_to_close:
      return
    # This maintains the same task context throughout cleanup
    for toolset in toolsets_to_close:
      try:
        logger.info('Closing toolset: %s', type(toolset).__name__)
        # Use asyncio.wait_for to add timeout protection
        await asyncio.wait_for(toolset.close(), timeout=10.0)
        logger.info('Successfully closed toolset: %s', type(toolset).__name__)
      except asyncio.TimeoutError:
        logger.warning('Toolset %s cleanup timed out', type(toolset).__name__)
      except Exception as e:
        logger.error('Error closing toolset %s: %s', type(toolset).__name__, e)
  async def close(self):
    """Closes the runner."""
    await self._cleanup_toolsets(self._collect_toolset(self.agent))
class InMemoryRunner(Runner):
  This runner uses in-memory implementations for artifact, session, and memory
  services, providing a lightweight and self-contained environment for agent
  execution.
  Attributes:
      agent: The root agent to run.
      app_name: The application name of the runner. Defaults to
        'InMemoryRunner'.
      _in_memory_session_service: Deprecated. Please don't use. The in-memory
        session service for the runner.
  """
  def __init__(self, agent: BaseAgent, *, app_name: str = 'InMemoryRunner'):
    """Initializes the InMemoryRunner.
    Args:
        agent: The root agent to run.
        app_name: The application name of the runner. Defaults to
          'InMemoryRunner'.
    """
    self._in_memory_session_service = InMemorySessionService()
    super().__init__(
        app_name=app_name,
        agent=agent,
        artifact_service=InMemoryArtifactService(),
        session_service=self._in_memory_session_service,
        memory_service=InMemoryMemoryService(),
    )
================================================
File: src/google/adk/telemetry.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# NOTE:
#
#    We expect that the underlying GenAI SDK will provide a certain
#    level of tracing and logging telemetry aligned with Open Telemetry
#    Semantic Conventions (such as logging prompts, responses,
#    request properties, etc.) and so the information that is recorded by the
#    Agent Development Kit should be focused on the higher-level
#    constructs of the framework that are not observable by the SDK.
from __future__ import annotations
import json
from typing import Any
from google.genai import types
from opentelemetry import trace
from .agents.invocation_context import InvocationContext
from .events.event import Event
from .models.llm_request import LlmRequest
from .models.llm_response import LlmResponse
from .tools.base_tool import BaseTool
tracer = trace.get_tracer('gcp.vertex.agent')
def _safe_json_serialize(obj) -> str:
  """Convert any Python object to a JSON-serializable type or string.
  Args:
    obj: The object to serialize.
  Returns:
    The JSON-serialized object string or <non-serializable> if the object cannot be serialized.
  """
  try:
    # Try direct JSON serialization first
    return json.dumps(
        obj, ensure_ascii=False, default=lambda o: '<not serializable>'
    )
  except (TypeError, OverflowError):
    return '<not serializable>'
def trace_tool_call(
    tool: BaseTool,
    args: dict[str, Any],
    function_response_event: Event,
):
  """Traces tool call.
  Args:
    tool: The tool that was called.
    args: The arguments to the tool call.
    function_response_event: The event with the function response details.
  """
  span = trace.get_current_span()
  span.set_attribute('gen_ai.system', 'gcp.vertex.agent')
  span.set_attribute('gen_ai.operation.name', 'execute_tool')
  span.set_attribute('gen_ai.tool.name', tool.name)
  span.set_attribute('gen_ai.tool.description', tool.description)
  tool_call_id = '<not specified>'
  tool_response = '<not specified>'
  if function_response_event.content.parts:
    function_response = function_response_event.content.parts[
        0
    ].function_response
    if function_response is not None:
      tool_call_id = function_response.id
      tool_response = function_response.response
  span.set_attribute('gen_ai.tool.call.id', tool_call_id)
  if not isinstance(tool_response, dict):
    tool_response = {'result': tool_response}
  span.set_attribute(
      'gcp.vertex.agent.tool_call_args',
      _safe_json_serialize(args),
  )
  span.set_attribute('gcp.vertex.agent.event_id', function_response_event.id)
  span.set_attribute(
      'gcp.vertex.agent.tool_response',
      _safe_json_serialize(tool_response),
  )
  # Setting empty llm request and response (as UI expect these) while not
  # applicable for tool_response.
  span.set_attribute('gcp.vertex.agent.llm_request', '{}')
  span.set_attribute(
      'gcp.vertex.agent.llm_response',
      '{}',
  )
def trace_merged_tool_calls(
    response_event_id: str,
    function_response_event: Event,
):
  """Traces merged tool call events.
  Calling this function is not needed for telemetry purposes. This is provided
  for preventing /debug/trace requests (typically sent by web UI).
  Args:
    response_event_id: The ID of the response event.
    function_response_event: The merged response event.
  """
  span = trace.get_current_span()
  span.set_attribute('gen_ai.system', 'gcp.vertex.agent')
  span.set_attribute('gen_ai.operation.name', 'execute_tool')
  span.set_attribute('gen_ai.tool.name', '(merged tools)')
  span.set_attribute('gen_ai.tool.description', '(merged tools)')
  span.set_attribute('gen_ai.tool.call.id', response_event_id)
  span.set_attribute('gcp.vertex.agent.tool_call_args', 'N/A')
  span.set_attribute('gcp.vertex.agent.event_id', response_event_id)
  try:
    function_response_event_json = function_response_event.model_dumps_json(
        exclude_none=True
    )
  except Exception:  # pylint: disable=broad-exception-caught
    function_response_event_json = '<not serializable>'
  span.set_attribute(
      'gcp.vertex.agent.tool_response',
      function_response_event_json,
  )
  # Setting empty llm request and response (as UI expect these) while not
  # applicable for tool_response.
  span.set_attribute('gcp.vertex.agent.llm_request', '{}')
  span.set_attribute(
      'gcp.vertex.agent.llm_response',
      '{}',
  )
def trace_call_llm(
    invocation_context: InvocationContext,
    event_id: str,
    llm_request: LlmRequest,
    llm_response: LlmResponse,
):
  """Traces a call to the LLM.
  This function records details about the LLM request and response as
  attributes on the current OpenTelemetry span.
  Args:
    invocation_context: The invocation context for the current agent run.
    event_id: The ID of the event.
    llm_request: The LLM request object.
    llm_response: The LLM response object.
  """
  span = trace.get_current_span()
  # Special standard Open Telemetry GenaI attributes that indicate
  # that this is a span related to a Generative AI system.
  span.set_attribute('gen_ai.system', 'gcp.vertex.agent')
  span.set_attribute('gen_ai.request.model', llm_request.model)
  span.set_attribute(
      'gcp.vertex.agent.invocation_id', invocation_context.invocation_id
  )
  span.set_attribute(
      'gcp.vertex.agent.session_id', invocation_context.session.id
  )
  span.set_attribute('gcp.vertex.agent.event_id', event_id)
  # Consider removing once GenAI SDK provides a way to record this info.
  span.set_attribute(
      'gcp.vertex.agent.llm_request',
      _safe_json_serialize(_build_llm_request_for_trace(llm_request)),
  )
  # Consider removing once GenAI SDK provides a way to record this info.
  try:
    llm_response_json = llm_response.model_dump_json(exclude_none=True)
  except Exception:  # pylint: disable=broad-exception-caught
    llm_response_json = '<not serializable>'
  span.set_attribute(
      'gcp.vertex.agent.llm_response',
      llm_response_json,
  )
def trace_send_data(
    invocation_context: InvocationContext,
    event_id: str,
    data: list[types.Content],
):
  """Traces the sending of data to the agent.
  This function records details about the data sent to the agent as
  attributes on the current OpenTelemetry span.
  Args:
    invocation_context: The invocation context for the current agent run.
    event_id: The ID of the event.
    data: A list of content objects.
  """
  span = trace.get_current_span()
  span.set_attribute(
      'gcp.vertex.agent.invocation_id', invocation_context.invocation_id
  )
  span.set_attribute('gcp.vertex.agent.event_id', event_id)
  # Once instrumentation is added to the GenAI SDK, consider whether this
  # information still needs to be recorded by the Agent Development Kit.
  span.set_attribute(
      'gcp.vertex.agent.data',
      _safe_json_serialize([
          types.Content(role=content.role, parts=content.parts).model_dump(
              exclude_none=True
          )
          for content in data
      ]),
  )
def _build_llm_request_for_trace(llm_request: LlmRequest) -> dict[str, Any]:
  """Builds a dictionary representation of the LLM request for tracing.
  This function prepares a dictionary representation of the LlmRequest
  object, suitable for inclusion in a trace. It excludes fields that cannot
  be serialized (e.g., function pointers) and avoids sending bytes data.
  Args:
    llm_request: The LlmRequest object.
  Returns:
    A dictionary representation of the LLM request.
  """
  # Some fields in LlmRequest are function pointers and can not be serialized.
  result = {
      'model': llm_request.model,
      'config': llm_request.config.model_dump(
          exclude_none=True, exclude='response_schema'
      ),
      'contents': [],
  }
  # We do not want to send bytes data to the trace.
  for content in llm_request.contents:
    parts = [part for part in content.parts if not part.inline_data]
    result['contents'].append(
        types.Content(role=content.role, parts=parts).model_dump(
            exclude_none=True
        )
    )
  return result
================================================
File: src/google/adk/version.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# version: date+base_cl
__version__ = "1.1.1"
================================================
File: src/google/adk/agents/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .base_agent import BaseAgent
from .live_request_queue import LiveRequest
from .live_request_queue import LiveRequestQueue
from .llm_agent import Agent
from .llm_agent import LlmAgent
from .loop_agent import LoopAgent
from .parallel_agent import ParallelAgent
from .run_config import RunConfig
from .sequential_agent import SequentialAgent
__all__ = [
    'Agent',
    'BaseAgent',
    'LlmAgent',
    'LoopAgent',
    'ParallelAgent',
    'SequentialAgent',
]
================================================
File: src/google/adk/agents/active_streaming_tool.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import asyncio
from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict
from .live_request_queue import LiveRequestQueue
class ActiveStreamingTool(BaseModel):
  """Manages streaming tool related resources during invocation."""
  model_config = ConfigDict(
      arbitrary_types_allowed=True,
      extra='forbid',
  )
  """The pydantic model config."""
  task: Optional[asyncio.Task] = None
  """The active task of this streaming tool."""
  stream: Optional[LiveRequestQueue] = None
  """The active (input) streams of this streaming tool."""
================================================
File: src/google/adk/agents/base_agent.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import inspect
from typing import Any
from typing import AsyncGenerator
from typing import Awaitable
from typing import Callable
from typing import final
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union
from google.genai import types
from opentelemetry import trace
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from typing_extensions import override
from typing_extensions import TypeAlias
from ..events.event import Event
from .callback_context import CallbackContext
if TYPE_CHECKING:
  from .invocation_context import InvocationContext
tracer = trace.get_tracer('gcp.vertex.agent')
_SingleAgentCallback: TypeAlias = Callable[
    [CallbackContext],
    Union[Awaitable[Optional[types.Content]], Optional[types.Content]],
]
BeforeAgentCallback: TypeAlias = Union[
    _SingleAgentCallback,
    list[_SingleAgentCallback],
]
AfterAgentCallback: TypeAlias = Union[
    _SingleAgentCallback,
    list[_SingleAgentCallback],
]
class BaseAgent(BaseModel):
  """Base class for all agents in Agent Development Kit."""
  model_config = ConfigDict(
      arbitrary_types_allowed=True,
      extra='forbid',
  )
  """The pydantic model config."""
  name: str
  """The agent's name.
  Agent name must be a Python identifier and unique within the agent tree.
  Agent name cannot be "user", since it's reserved for end-user's input.
  """
  description: str = ''
  """Description about the agent's capability.
  The model uses this to determine whether to delegate control to the agent.
  One-line description is enough and preferred.
  """
  parent_agent: Optional[BaseAgent] = Field(default=None, init=False)
  """The parent agent of this agent.
  Note that an agent can ONLY be added as sub-agent once.
  If you want to add one agent twice as sub-agent, consider to create two agent
  instances with identical config, but with different name and add them to the
  agent tree.
  """
  sub_agents: list[BaseAgent] = Field(default_factory=list)
  """The sub-agents of this agent."""
  before_agent_callback: Optional[BeforeAgentCallback] = None
  """Callback or list of callbacks to be invoked before the agent run.
  When a list of callbacks is provided, the callbacks will be called in the
  order they are listed until a callback does not return None.
  Args:
    callback_context: MUST be named 'callback_context' (enforced).
  Returns:
    Optional[types.Content]: The content to return to the user.
      When the content is present, the agent run will be skipped and the
      provided content will be returned to user.
  """
  after_agent_callback: Optional[AfterAgentCallback] = None
  """Callback or list of callbacks to be invoked after the agent run.
  When a list of callbacks is provided, the callbacks will be called in the
  order they are listed until a callback does not return None.
  Args:
    callback_context: MUST be named 'callback_context' (enforced).
  Returns:
    Optional[types.Content]: The content to return to the user.
      When the content is present, the provided content will be used as agent
      response and appended to event history as agent response.
  """
  @final
  async def run_async(
      self,
      parent_context: InvocationContext,
  ) -> AsyncGenerator[Event, None]:
    """Entry method to run an agent via text-based conversation.
    Args:
      parent_context: InvocationContext, the invocation context of the parent
        agent.
    Yields:
      Event: the events generated by the agent.
    """
    with tracer.start_as_current_span(f'agent_run [{self.name}]'):
      ctx = self._create_invocation_context(parent_context)
      if event := await self.__handle_before_agent_callback(ctx):
        yield event
      if ctx.end_invocation:
        return
      async for event in self._run_async_impl(ctx):
        yield event
      if ctx.end_invocation:
        return
      if event := await self.__handle_after_agent_callback(ctx):
        yield event
  @final
  async def run_live(
      self,
      parent_context: InvocationContext,
  ) -> AsyncGenerator[Event, None]:
    """Entry method to run an agent via video/audio-based conversation.
    Args:
      parent_context: InvocationContext, the invocation context of the parent
        agent.
    Yields:
      Event: the events generated by the agent.
    """
    with tracer.start_as_current_span(f'agent_run [{self.name}]'):
      ctx = self._create_invocation_context(parent_context)
      # TODO(hangfei): support before/after_agent_callback
      async for event in self._run_live_impl(ctx):
        yield event
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    """Core logic to run this agent via text-based conversation.
    Args:
      ctx: InvocationContext, the invocation context for this agent.
    Yields:
      Event: the events generated by the agent.
    """
    raise NotImplementedError(
        f'_run_async_impl for {type(self)} is not implemented.'
    )
    yield  # AsyncGenerator requires having at least one yield statement
  async def _run_live_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    """Core logic to run this agent via video/audio-based conversation.
    Args:
      ctx: InvocationContext, the invocation context for this agent.
    Yields:
      Event: the events generated by the agent.
    """
    raise NotImplementedError(
        f'_run_live_impl for {type(self)} is not implemented.'
    )
    yield  # AsyncGenerator requires having at least one yield statement
  @property
  def root_agent(self) -> BaseAgent:
    """Gets the root agent of this agent."""
    root_agent = self
    while root_agent.parent_agent is not None:
      root_agent = root_agent.parent_agent
    return root_agent
  def find_agent(self, name: str) -> Optional[BaseAgent]:
    """Finds the agent with the given name in this agent and its descendants.
    Args:
      name: The name of the agent to find.
    Returns:
      The agent with the matching name, or None if no such agent is found.
    """
    if self.name == name:
      return self
    return self.find_sub_agent(name)
  def find_sub_agent(self, name: str) -> Optional[BaseAgent]:
    """Finds the agent with the given name in this agent's descendants.
    Args:
      name: The name of the agent to find.
    Returns:
      The agent with the matching name, or None if no such agent is found.
    """
    for sub_agent in self.sub_agents:
      if result := sub_agent.find_agent(name):
        return result
    return None
  def _create_invocation_context(
      self, parent_context: InvocationContext
  ) -> InvocationContext:
    """Creates a new invocation context for this agent."""
    invocation_context = parent_context.model_copy(update={'agent': self})
    if parent_context.branch:
      invocation_context.branch = f'{parent_context.branch}.{self.name}'
    return invocation_context
  @property
  def canonical_before_agent_callbacks(self) -> list[_SingleAgentCallback]:
    """The resolved self.before_agent_callback field as a list of _SingleAgentCallback.
    This method is only for use by Agent Development Kit.
    """
    if not self.before_agent_callback:
      return []
    if isinstance(self.before_agent_callback, list):
      return self.before_agent_callback
    return [self.before_agent_callback]
  @property
  def canonical_after_agent_callbacks(self) -> list[_SingleAgentCallback]:
    """The resolved self.after_agent_callback field as a list of _SingleAgentCallback.
    This method is only for use by Agent Development Kit.
    """
    if not self.after_agent_callback:
      return []
    if isinstance(self.after_agent_callback, list):
      return self.after_agent_callback
    return [self.after_agent_callback]
  async def __handle_before_agent_callback(
      self, ctx: InvocationContext
  ) -> Optional[Event]:
    """Runs the before_agent_callback if it exists.
    Returns:
      Optional[Event]: an event if callback provides content or changed state.
    """
    ret_event = None
    if not self.canonical_before_agent_callbacks:
      return ret_event
    callback_context = CallbackContext(ctx)
    for callback in self.canonical_before_agent_callbacks:
      before_agent_callback_content = callback(
          callback_context=callback_context
      )
      if inspect.isawaitable(before_agent_callback_content):
        before_agent_callback_content = await before_agent_callback_content
      if before_agent_callback_content:
        ret_event = Event(
            invocation_id=ctx.invocation_id,
            author=self.name,
            branch=ctx.branch,
            content=before_agent_callback_content,
            actions=callback_context._event_actions,
        )
        ctx.end_invocation = True
        return ret_event
    if callback_context.state.has_delta():
      ret_event = Event(
          invocation_id=ctx.invocation_id,
          author=self.name,
          branch=ctx.branch,
          actions=callback_context._event_actions,
      )
    return ret_event
  async def __handle_after_agent_callback(
      self, invocation_context: InvocationContext
  ) -> Optional[Event]:
    """Runs the after_agent_callback if it exists.
    Returns:
      Optional[Event]: an event if callback provides content or changed state.
    """
    ret_event = None
    if not self.canonical_after_agent_callbacks:
      return ret_event
    callback_context = CallbackContext(invocation_context)
    for callback in self.canonical_after_agent_callbacks:
      after_agent_callback_content = callback(callback_context=callback_context)
      if inspect.isawaitable(after_agent_callback_content):
        after_agent_callback_content = await after_agent_callback_content
      if after_agent_callback_content:
        ret_event = Event(
            invocation_id=invocation_context.invocation_id,
            author=self.name,
            branch=invocation_context.branch,
            content=after_agent_callback_content,
            actions=callback_context._event_actions,
        )
        return ret_event
    if callback_context.state.has_delta():
      ret_event = Event(
          invocation_id=invocation_context.invocation_id,
          author=self.name,
          branch=invocation_context.branch,
          content=after_agent_callback_content,
          actions=callback_context._event_actions,
      )
    return ret_event
  @override
  def model_post_init(self, __context: Any) -> None:
    self.__set_parent_agent_for_sub_agents()
  @field_validator('name', mode='after')
  @classmethod
  def __validate_name(cls, value: str):
    if not value.isidentifier():
      raise ValueError(
          f'Found invalid agent name: `{value}`.'
          ' Agent name must be a valid identifier. It should start with a'
          ' letter (a-z, A-Z) or an underscore (_), and can only contain'
          ' letters, digits (0-9), and underscores.'
      )
    if value == 'user':
      raise ValueError(
          "Agent name cannot be `user`. `user` is reserved for end-user's"
          ' input.'
      )
    return value
  def __set_parent_agent_for_sub_agents(self) -> BaseAgent:
    for sub_agent in self.sub_agents:
      if sub_agent.parent_agent is not None:
        raise ValueError(
            f'Agent `{sub_agent.name}` already has a parent agent, current'
            f' parent: `{sub_agent.parent_agent.name}`, trying to add:'
            f' `{self.name}`'
        )
      sub_agent.parent_agent = self
    return self
================================================
File: src/google/adk/agents/callback_context.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import Optional
from typing import TYPE_CHECKING
from typing_extensions import override
from .readonly_context import ReadonlyContext
if TYPE_CHECKING:
  from google.genai import types
  from ..events.event_actions import EventActions
  from ..sessions.state import State
  from .invocation_context import InvocationContext
class CallbackContext(ReadonlyContext):
  """The context of various callbacks within an agent run."""
  def __init__(
      self,
      invocation_context: InvocationContext,
      *,
      event_actions: Optional[EventActions] = None,
  ) -> None:
    super().__init__(invocation_context)
    from ..events.event_actions import EventActions
    from ..sessions.state import State
    # TODO(weisun): make this public for Agent Development Kit, but private for
    # users.
    self._event_actions = event_actions or EventActions()
    self._state = State(
        value=invocation_context.session.state,
        delta=self._event_actions.state_delta,
    )
  @property
  @override
  def state(self) -> State:
    """The delta-aware state of the current session.
    For any state change, you can mutate this object directly,
    e.g. `ctx.state['foo'] = 'bar'`
    """
    return self._state
  async def load_artifact(
      self, filename: str, version: Optional[int] = None
  ) -> Optional[types.Part]:
    """Loads an artifact attached to the current session.
    Args:
      filename: The filename of the artifact.
        returned.
    Returns:
      The artifact.
    """
    if self._invocation_context.artifact_service is None:
      raise ValueError("Artifact service is not initialized.")
    return await self._invocation_context.artifact_service.load_artifact(
        app_name=self._invocation_context.app_name,
        user_id=self._invocation_context.user_id,
        session_id=self._invocation_context.session.id,
        filename=filename,
        version=version,
    )
  async def save_artifact(self, filename: str, artifact: types.Part) -> int:
    """Saves an artifact and records it as delta for the current session.
    Args:
      filename: The filename of the artifact.
      artifact: The artifact to save.
    Returns:
     The version of the artifact.
    """
    if self._invocation_context.artifact_service is None:
      raise ValueError("Artifact service is not initialized.")
    version = await self._invocation_context.artifact_service.save_artifact(
        app_name=self._invocation_context.app_name,
        user_id=self._invocation_context.user_id,
        session_id=self._invocation_context.session.id,
        filename=filename,
        artifact=artifact,
    )
    self._event_actions.artifact_delta[filename] = version
    return version
================================================
File: src/google/adk/agents/invocation_context.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import Optional
import uuid
from google.genai import types
from pydantic import BaseModel
from pydantic import ConfigDict
from ..artifacts.base_artifact_service import BaseArtifactService
from ..memory.base_memory_service import BaseMemoryService
from ..sessions.base_session_service import BaseSessionService
from ..sessions.session import Session
from .active_streaming_tool import ActiveStreamingTool
from .base_agent import BaseAgent
from .live_request_queue import LiveRequestQueue
from .run_config import RunConfig
from .transcription_entry import TranscriptionEntry
class LlmCallsLimitExceededError(Exception):
  """Error thrown when the number of LLM calls exceed the limit."""
class _InvocationCostManager(BaseModel):
  """A container to keep track of the cost of invocation.
  While we don't expect the metrics captured here to be a direct
  representative of monetary cost incurred in executing the current
  invocation, they in some ways have an indirect effect.
  """
  _number_of_llm_calls: int = 0
  """A counter that keeps track of number of llm calls made."""
  def increment_and_enforce_llm_calls_limit(
      self, run_config: Optional[RunConfig]
  ):
    """Increments _number_of_llm_calls and enforces the limit."""
    # We first increment the counter and then check the conditions.
    self._number_of_llm_calls += 1
    if (
        run_config
        and run_config.max_llm_calls > 0
        and self._number_of_llm_calls > run_config.max_llm_calls
    ):
      # We only enforce the limit if the limit is a positive number.
      raise LlmCallsLimitExceededError(
          "Max number of llm calls limit of"
          f" `{run_config.max_llm_calls}` exceeded"
      )
class InvocationContext(BaseModel):
  """An invocation context represents the data of a single invocation of an agent.
  An invocation:
    1. Starts with a user message and ends with a final response.
    2. Can contain one or multiple agent calls.
    3. Is handled by runner.run_async().
  An invocation runs an agent until it does not request to transfer to another
  agent.
  An agent call:
    1. Is handled by agent.run().
    2. Ends when agent.run() ends.
  An LLM agent call is an agent with a BaseLLMFlow.
  An LLM agent call can contain one or multiple steps.
  An LLM agent runs steps in a loop until:
    1. A final response is generated.
    2. The agent transfers to another agent.
    3. The end_invocation is set to true by any callbacks or tools.
  A step:
    1. Calls the LLM only once and yields its response.
    2. Calls the tools and yields their responses if requested.
  The summarization of the function response is considered another step, since
  it is another llm call.
  A step ends when it's done calling llm and tools, or if the end_invocation
  is set to true at any time.
  ```
     ┌─────────────────────── invocation ──────────────────────────┐
     ┌──────────── llm_agent_call_1 ────────────┐ ┌─ agent_call_2 ─┐
     ┌──── step_1 ────────┐ ┌───── step_2 ──────┐
     [call_llm] [call_tool] [call_llm] [transfer]
  ```
  """
  model_config = ConfigDict(
      arbitrary_types_allowed=True,
      extra="forbid",
  )
  """The pydantic model config."""
  artifact_service: Optional[BaseArtifactService] = None
  session_service: BaseSessionService
  memory_service: Optional[BaseMemoryService] = None
  invocation_id: str
  """The id of this invocation context. Readonly."""
  branch: Optional[str] = None
  """The branch of the invocation context.
  The format is like agent_1.agent_2.agent_3, where agent_1 is the parent of
  agent_2, and agent_2 is the parent of agent_3.
  Branch is used when multiple sub-agents shouldn't see their peer agents'
  conversation history.
  """
  agent: BaseAgent
  """The current agent of this invocation context. Readonly."""
  user_content: Optional[types.Content] = None
  """The user content that started this invocation. Readonly."""
  session: Session
  """The current session of this invocation context. Readonly."""
  end_invocation: bool = False
  """Whether to end this invocation.
  Set to True in callbacks or tools to terminate this invocation."""
  live_request_queue: Optional[LiveRequestQueue] = None
  """The queue to receive live requests."""
  active_streaming_tools: Optional[dict[str, ActiveStreamingTool]] = None
  """The running streaming tools of this invocation."""
  transcription_cache: Optional[list[TranscriptionEntry]] = None
  """Caches necessary, data audio or contents, that are needed by transcription."""
  run_config: Optional[RunConfig] = None
  """Configurations for live agents under this invocation."""
  _invocation_cost_manager: _InvocationCostManager = _InvocationCostManager()
  """A container to keep track of different kinds of costs incurred as a part
  of this invocation.
  """
  def increment_llm_call_count(
      self,
  ):
    """Tracks number of llm calls made.
    Raises:
      LlmCallsLimitExceededError: If number of llm calls made exceed the set
        threshold.
    """
    self._invocation_cost_manager.increment_and_enforce_llm_calls_limit(
        self.run_config
    )
  @property
  def app_name(self) -> str:
    return self.session.app_name
  @property
  def user_id(self) -> str:
    return self.session.user_id
def new_invocation_context_id() -> str:
  return "e-" + str(uuid.uuid4())
================================================
File: src/google/adk/agents/langgraph_agent.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import AsyncGenerator
from typing import Union
from google.genai import types
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.graph import CompiledGraph
from pydantic import ConfigDict
from typing_extensions import override
from ..events.event import Event
from .base_agent import BaseAgent
from .invocation_context import InvocationContext
def _get_last_human_messages(events: list[Event]) -> list[HumanMessage]:
  """Extracts last human messages from given list of events.
  Args:
    events: the list of events
  Returns:
    list of last human messages
  """
  messages = []
  for event in reversed(events):
    if messages and event.author != 'user':
      break
    if event.author == 'user' and event.content and event.content.parts:
      messages.append(HumanMessage(content=event.content.parts[0].text))
  return list(reversed(messages))
class LangGraphAgent(BaseAgent):
  """Currently a concept implementation, supports single and multi-turn."""
  model_config = ConfigDict(
      arbitrary_types_allowed=True,
  )
  """The pydantic model config."""
  graph: CompiledGraph
  instruction: str = ''
  @override
  async def _run_async_impl(
      self,
      ctx: InvocationContext,
  ) -> AsyncGenerator[Event, None]:
    # Needed for langgraph checkpointer (for subsequent invocations; multi-turn)
    config: RunnableConfig = {'configurable': {'thread_id': ctx.session.id}}
    # Add instruction as SystemMessage if graph state is empty
    current_graph_state = self.graph.get_state(config)
    graph_messages = (
        current_graph_state.values.get('messages', [])
        if current_graph_state.values
        else []
    )
    messages = (
        [SystemMessage(content=self.instruction)]
        if self.instruction and not graph_messages
        else []
    )
    # Add events to messages (evaluating the memory used; parent agent vs checkpointer)
    messages += self._get_messages(ctx.session.events)
    # Use the Runnable
    final_state = self.graph.invoke({'messages': messages}, config)
    result = final_state['messages'][-1].content
    result_event = Event(
        invocation_id=ctx.invocation_id,
        author=self.name,
        branch=ctx.branch,
        content=types.Content(
            role='model',
            parts=[types.Part.from_text(text=result)],
        ),
    )
    yield result_event
  def _get_messages(
      self, events: list[Event]
  ) -> list[Union[HumanMessage, AIMessage]]:
    """Extracts messages from given list of events.
    If the developer provides their own memory within langgraph, we return the
    last user messages only. Otherwise, we return all messages between the user
    and the agent.
    Args:
      events: the list of events
    Returns:
      list of messages
    """
    if self.graph.checkpointer:
      return _get_last_human_messages(events)
    else:
      return self._get_conversation_with_agent(events)
  def _get_conversation_with_agent(
      self, events: list[Event]
  ) -> list[Union[HumanMessage, AIMessage]]:
    """Extracts messages from given list of events.
    Args:
      events: the list of events
    Returns:
      list of messages
    """
    messages = []
    for event in events:
      if not event.content or not event.content.parts:
        continue
      if event.author == 'user':
        messages.append(HumanMessage(content=event.content.parts[0].text))
      elif event.author == self.name:
        messages.append(AIMessage(content=event.content.parts[0].text))
    return messages
================================================
File: src/google/adk/agents/live_request_queue.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Optional
from google.genai import types
from pydantic import BaseModel
from pydantic import ConfigDict
class LiveRequest(BaseModel):
  """Request send to live agents."""
  model_config = ConfigDict(ser_json_bytes='base64', val_json_bytes='base64')
  """The pydantic model config."""
  content: Optional[types.Content] = None
  """If set, send the content to the model in turn-by-turn mode."""
  blob: Optional[types.Blob] = None
  """If set, send the blob to the model in realtime mode."""
  close: bool = False
  """If set, close the queue. queue.shutdown() is only supported in Python 3.13+."""
class LiveRequestQueue:
  """Queue used to send LiveRequest in a live(bidirectional streaming) way."""
  def __init__(self):
    # Ensure there's an event loop available in this thread
    try:
      asyncio.get_running_loop()
    except RuntimeError:
      # No running loop, create one
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
    # Now create the queue (it will use the event loop we just ensured exists)
    self._queue = asyncio.Queue()
  def close(self):
    self._queue.put_nowait(LiveRequest(close=True))
  def send_content(self, content: types.Content):
    self._queue.put_nowait(LiveRequest(content=content))
  def send_realtime(self, blob: types.Blob):
    self._queue.put_nowait(LiveRequest(blob=blob))
  def send(self, req: LiveRequest):
    self._queue.put_nowait(req)
  async def get(self) -> LiveRequest:
    return await self._queue.get()
================================================
File: src/google/adk/agents/llm_agent.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import inspect
import logging
from typing import Any
from typing import AsyncGenerator
from typing import Awaitable
from typing import Callable
from typing import Literal
from typing import Optional
from typing import Union
from google.genai import types
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from typing_extensions import override
from typing_extensions import TypeAlias
from ..code_executors.base_code_executor import BaseCodeExecutor
from ..events.event import Event
from ..examples.base_example_provider import BaseExampleProvider
from ..examples.example import Example
from ..flows.llm_flows.auto_flow import AutoFlow
from ..flows.llm_flows.base_llm_flow import BaseLlmFlow
from ..flows.llm_flows.single_flow import SingleFlow
from ..models.base_llm import BaseLlm
from ..models.llm_request import LlmRequest
from ..models.llm_response import LlmResponse
from ..models.registry import LLMRegistry
from ..planners.base_planner import BasePlanner
from ..tools.base_tool import BaseTool
from ..tools.base_toolset import BaseToolset
from ..tools.function_tool import FunctionTool
from ..tools.tool_context import ToolContext
from .base_agent import BaseAgent
from .callback_context import CallbackContext
from .invocation_context import InvocationContext
from .readonly_context import ReadonlyContext
logger = logging.getLogger('google_adk.' + __name__)
_SingleBeforeModelCallback: TypeAlias = Callable[
    [CallbackContext, LlmRequest],
    Union[Awaitable[Optional[LlmResponse]], Optional[LlmResponse]],
]
BeforeModelCallback: TypeAlias = Union[
    _SingleBeforeModelCallback,
    list[_SingleBeforeModelCallback],
]
_SingleAfterModelCallback: TypeAlias = Callable[
    [CallbackContext, LlmResponse],
    Union[Awaitable[Optional[LlmResponse]], Optional[LlmResponse]],
]
AfterModelCallback: TypeAlias = Union[
    _SingleAfterModelCallback,
    list[_SingleAfterModelCallback],
]
_SingleBeforeToolCallback: TypeAlias = Callable[
    [BaseTool, dict[str, Any], ToolContext],
    Union[Awaitable[Optional[dict]], Optional[dict]],
]
BeforeToolCallback: TypeAlias = Union[
    _SingleBeforeToolCallback,
    list[_SingleBeforeToolCallback],
]
_SingleAfterToolCallback: TypeAlias = Callable[
    [BaseTool, dict[str, Any], ToolContext, dict],
    Union[Awaitable[Optional[dict]], Optional[dict]],
]
AfterToolCallback: TypeAlias = Union[
    _SingleAfterToolCallback,
    list[_SingleAfterToolCallback],
]
InstructionProvider: TypeAlias = Callable[
    [ReadonlyContext], Union[str, Awaitable[str]]
]
ToolUnion: TypeAlias = Union[Callable, BaseTool, BaseToolset]
ExamplesUnion = Union[list[Example], BaseExampleProvider]
async def _convert_tool_union_to_tools(
    tool_union: ToolUnion, ctx: ReadonlyContext
) -> list[BaseTool]:
  if isinstance(tool_union, BaseTool):
    return [tool_union]
  if isinstance(tool_union, Callable):
    return [FunctionTool(func=tool_union)]
  return await tool_union.get_tools(ctx)
class LlmAgent(BaseAgent):
  """LLM-based Agent."""
  model: Union[str, BaseLlm] = ''
  """The model to use for the agent.
  When not set, the agent will inherit the model from its ancestor.
  """
  instruction: Union[str, InstructionProvider] = ''
  """Instructions for the LLM model, guiding the agent's behavior."""
  global_instruction: Union[str, InstructionProvider] = ''
  """Instructions for all the agents in the entire agent tree.
  global_instruction ONLY takes effect in root agent.
  For example: use global_instruction to make all agents have a stable identity
  or personality.
  """
  tools: list[ToolUnion] = Field(default_factory=list)
  """Tools available to this agent."""
  generate_content_config: Optional[types.GenerateContentConfig] = None
  """The additional content generation configurations.
  NOTE: not all fields are usable, e.g. tools must be configured via `tools`,
  thinking_config must be configured via `planner` in LlmAgent.
  For example: use this config to adjust model temperature, configure safety
  settings, etc.
  """
  # LLM-based agent transfer configs - Start
  disallow_transfer_to_parent: bool = False
  """Disallows LLM-controlled transferring to the parent agent.
  NOTE: Setting this as True also prevents this agent to continue reply to the
  end-user. This behavior prevents one-way transfer, in which end-user may be
  stuck with one agent that cannot transfer to other agents in the agent tree.
  """
  disallow_transfer_to_peers: bool = False
  """Disallows LLM-controlled transferring to the peer agents."""
  # LLM-based agent transfer configs - End
  include_contents: Literal['default', 'none'] = 'default'
  """Whether to include contents in the model request.
  When set to 'none', the model request will not include any contents, such as
  user messages, tool results, etc.
  """
  # Controlled input/output configurations - Start
  input_schema: Optional[type[BaseModel]] = None
  """The input schema when agent is used as a tool."""
  output_schema: Optional[type[BaseModel]] = None
  """The output schema when agent replies.
  NOTE: when this is set, agent can ONLY reply and CANNOT use any tools, such as
  function tools, RAGs, agent transfer, etc.
  """
  output_key: Optional[str] = None
  """The key in session state to store the output of the agent.
  Typically use cases:
  - Extracts agent reply for later use, such as in tools, callbacks, etc.
  - Connects agents to coordinate with each other.
  """
  # Controlled input/output configurations - End
  # Advance features - Start
  planner: Optional[BasePlanner] = None
  """Instructs the agent to make a plan and execute it step by step.
  NOTE: to use model's built-in thinking features, set the `thinking_config`
  field in `google.adk.planners.built_in_planner`.
  """
  code_executor: Optional[BaseCodeExecutor] = None
  """Allow agent to execute code blocks from model responses using the provided
  CodeExecutor.
  Check out available code executions in `google.adk.code_executor` package.
  NOTE: to use model's built-in code executor, use the `BuiltInCodeExecutor`.
  """
  # Advance features - End
  # TODO: remove below fields after migration. - Start
  # These fields are added back for easier migration.
  examples: Optional[ExamplesUnion] = None
  # TODO: remove above fields after migration. - End
  # Callbacks - Start
  before_model_callback: Optional[BeforeModelCallback] = None
  """Callback or list of callbacks to be called before calling the LLM.
  When a list of callbacks is provided, the callbacks will be called in the
  order they are listed until a callback does not return None.
  Args:
    callback_context: CallbackContext,
    llm_request: LlmRequest, The raw model request. Callback can mutate the
    request.
  Returns:
    The content to return to the user. When present, the model call will be
    skipped and the provided content will be returned to user.
  """
  after_model_callback: Optional[AfterModelCallback] = None
  """Callback or list of callbacks to be called after calling the LLM.
  When a list of callbacks is provided, the callbacks will be called in the
  order they are listed until a callback does not return None.
  Args:
    callback_context: CallbackContext,
    llm_response: LlmResponse, the actual model response.
  Returns:
    The content to return to the user. When present, the actual model response
    will be ignored and the provided content will be returned to user.
  """
  before_tool_callback: Optional[BeforeToolCallback] = None
  """Callback or list of callbacks to be called before calling the tool.
  When a list of callbacks is provided, the callbacks will be called in the
  order they are listed until a callback does not return None.
  Args:
    tool: The tool to be called.
    args: The arguments to the tool.
    tool_context: ToolContext,
  Returns:
    The tool response. When present, the returned tool response will be used and
    the framework will skip calling the actual tool.
  """
  after_tool_callback: Optional[AfterToolCallback] = None
  """Callback or list of callbacks to be called after calling the tool.
  When a list of callbacks is provided, the callbacks will be called in the
  order they are listed until a callback does not return None.
  Args:
    tool: The tool to be called.
    args: The arguments to the tool.
    tool_context: ToolContext,
    tool_response: The response from the tool.
  Returns:
    When present, the returned dict will be used as tool result.
  """
  # Callbacks - End
  @override
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    async for event in self._llm_flow.run_async(ctx):
      self.__maybe_save_output_to_state(event)
      yield event
  @override
  async def _run_live_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    async for event in self._llm_flow.run_live(ctx):
      self.__maybe_save_output_to_state(event)
      yield event
    if ctx.end_invocation:
      return
  @property
  def canonical_model(self) -> BaseLlm:
    """The resolved self.model field as BaseLlm.
    This method is only for use by Agent Development Kit.
    """
    if isinstance(self.model, BaseLlm):
      return self.model
    elif self.model:  # model is non-empty str
      return LLMRegistry.new_llm(self.model)
    else:  # find model from ancestors.
      ancestor_agent = self.parent_agent
      while ancestor_agent is not None:
        if isinstance(ancestor_agent, LlmAgent):
          return ancestor_agent.canonical_model
        ancestor_agent = ancestor_agent.parent_agent
      raise ValueError(f'No model found for {self.name}.')
  async def canonical_instruction(
      self, ctx: ReadonlyContext
  ) -> tuple[str, bool]:
    """The resolved self.instruction field to construct instruction for this agent.
    This method is only for use by Agent Development Kit.
    Args:
      ctx: The context to retrieve the session state.
    Returns:
      A tuple of (instruction, bypass_state_injection).
      instruction: The resolved self.instruction field.
      bypass_state_injection: Whether the instruction is based on
      InstructionProvider.
    """
    if isinstance(self.instruction, str):
      return self.instruction, False
    else:
      instruction = self.instruction(ctx)
      if inspect.isawaitable(instruction):
        instruction = await instruction
      return instruction, True
  async def canonical_global_instruction(
      self, ctx: ReadonlyContext
  ) -> tuple[str, bool]:
    """The resolved self.instruction field to construct global instruction.
    This method is only for use by Agent Development Kit.
    Args:
      ctx: The context to retrieve the session state.
    Returns:
      A tuple of (instruction, bypass_state_injection).
      instruction: The resolved self.global_instruction field.
      bypass_state_injection: Whether the instruction is based on
      InstructionProvider.
    """
    if isinstance(self.global_instruction, str):
      return self.global_instruction, False
    else:
      global_instruction = self.global_instruction(ctx)
      if inspect.isawaitable(global_instruction):
        global_instruction = await global_instruction
      return global_instruction, True
  async def canonical_tools(
      self, ctx: ReadonlyContext = None
  ) -> list[BaseTool]:
    """The resolved self.tools field as a list of BaseTool based on the context.
    This method is only for use by Agent Development Kit.
    """
    resolved_tools = []
    for tool_union in self.tools:
      resolved_tools.extend(await _convert_tool_union_to_tools(tool_union, ctx))
    return resolved_tools
  @property
  def canonical_before_model_callbacks(
      self,
  ) -> list[_SingleBeforeModelCallback]:
    """The resolved self.before_model_callback field as a list of _SingleBeforeModelCallback.
    This method is only for use by Agent Development Kit.
    """
    if not self.before_model_callback:
      return []
    if isinstance(self.before_model_callback, list):
      return self.before_model_callback
    return [self.before_model_callback]
  @property
  def canonical_after_model_callbacks(self) -> list[_SingleAfterModelCallback]:
    """The resolved self.after_model_callback field as a list of _SingleAfterModelCallback.
    This method is only for use by Agent Development Kit.
    """
    if not self.after_model_callback:
      return []
    if isinstance(self.after_model_callback, list):
      return self.after_model_callback
    return [self.after_model_callback]
  @property
  def canonical_before_tool_callbacks(
      self,
  ) -> list[BeforeToolCallback]:
    """The resolved self.before_tool_callback field as a list of BeforeToolCallback.
    This method is only for use by Agent Development Kit.
    """
    if not self.before_tool_callback:
      return []
    if isinstance(self.before_tool_callback, list):
      return self.before_tool_callback
    return [self.before_tool_callback]
  @property
  def canonical_after_tool_callbacks(
      self,
  ) -> list[AfterToolCallback]:
    """The resolved self.after_tool_callback field as a list of AfterToolCallback.
    This method is only for use by Agent Development Kit.
    """
    if not self.after_tool_callback:
      return []
    if isinstance(self.after_tool_callback, list):
      return self.after_tool_callback
    return [self.after_tool_callback]
  @property
  def _llm_flow(self) -> BaseLlmFlow:
    if (
        self.disallow_transfer_to_parent
        and self.disallow_transfer_to_peers
        and not self.sub_agents
    ):
      return SingleFlow()
    else:
      return AutoFlow()
  def __maybe_save_output_to_state(self, event: Event):
    """Saves the model output to state if needed."""
    if (
        self.output_key
        and event.is_final_response()
        and event.content
        and event.content.parts
    ):
      result = ''.join(
          [part.text if part.text else '' for part in event.content.parts]
      )
      if self.output_schema:
        result = self.output_schema.model_validate_json(result).model_dump(
            exclude_none=True
        )
      event.actions.state_delta[self.output_key] = result
  @model_validator(mode='after')
  def __model_validator_after(self) -> LlmAgent:
    self.__check_output_schema()
    return self
  def __check_output_schema(self):
    if not self.output_schema:
      return
    if (
        not self.disallow_transfer_to_parent
        or not self.disallow_transfer_to_peers
    ):
      logger.warning(
          'Invalid config for agent %s: output_schema cannot co-exist with'
          ' agent transfer configurations. Setting'
          ' disallow_transfer_to_parent=True, disallow_transfer_to_peers=True',
          self.name,
      )
      self.disallow_transfer_to_parent = True
      self.disallow_transfer_to_peers = True
    if self.sub_agents:
      raise ValueError(
          f'Invalid config for agent {self.name}: if output_schema is set,'
          ' sub_agents must be empty to disable agent transfer.'
      )
    if self.tools:
      raise ValueError(
          f'Invalid config for agent {self.name}: if output_schema is set,'
          ' tools must be empty'
      )
  @field_validator('generate_content_config', mode='after')
  @classmethod
  def __validate_generate_content_config(
      cls, generate_content_config: Optional[types.GenerateContentConfig]
  ) -> types.GenerateContentConfig:
    if not generate_content_config:
      return types.GenerateContentConfig()
    if generate_content_config.thinking_config:
      raise ValueError('Thinking config should be set via LlmAgent.planner.')
    if generate_content_config.tools:
      raise ValueError('All tools must be set via LlmAgent.tools.')
    if generate_content_config.system_instruction:
      raise ValueError(
          'System instruction must be set via LlmAgent.instruction.'
      )
    if generate_content_config.response_schema:
      raise ValueError(
          'Response schema must be set via LlmAgent.output_schema.'
      )
    return generate_content_config
Agent: TypeAlias = LlmAgent
================================================
File: src/google/adk/agents/loop_agent.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Loop agent implementation."""
from __future__ import annotations
from typing import AsyncGenerator
from typing import Optional
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from ..events.event import Event
from .base_agent import BaseAgent
class LoopAgent(BaseAgent):
  """A shell agent that run its sub-agents in a loop.
  When sub-agent generates an event with escalate or max_iterations are
  reached, the loop agent will stop.
  """
  max_iterations: Optional[int] = None
  """The maximum number of iterations to run the loop agent.
  If not set, the loop agent will run indefinitely until a sub-agent
  escalates.
  """
  @override
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    times_looped = 0
    while not self.max_iterations or times_looped < self.max_iterations:
      for sub_agent in self.sub_agents:
        async for event in sub_agent.run_async(ctx):
          yield event
          if event.actions.escalate:
            return
      times_looped += 1
    return
  @override
  async def _run_live_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    raise NotImplementedError('This is not supported yet for LoopAgent.')
    yield  # AsyncGenerator requires having at least one yield statement
================================================
File: src/google/adk/agents/parallel_agent.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Parallel agent implementation."""
from __future__ import annotations
import asyncio
from typing import AsyncGenerator
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from ..events.event import Event
from .base_agent import BaseAgent
def _set_branch_for_current_agent(
    current_agent: BaseAgent, invocation_context: InvocationContext
):
  invocation_context.branch = (
      f"{invocation_context.branch}.{current_agent.name}"
      if invocation_context.branch
      else current_agent.name
  )
async def _merge_agent_run(
    agent_runs: list[AsyncGenerator[Event, None]],
) -> AsyncGenerator[Event, None]:
  """Merges the agent run event generator.
  This implementation guarantees for each agent, it won't move on until the
  generated event is processed by upstream runner.
  Args:
      agent_runs: A list of async generators that yield events from each agent.
  Yields:
      Event: The next event from the merged generator.
  """
  tasks = [
      asyncio.create_task(events_for_one_agent.__anext__())
      for events_for_one_agent in agent_runs
  ]
  pending_tasks = set(tasks)
  while pending_tasks:
    done, pending_tasks = await asyncio.wait(
        pending_tasks, return_when=asyncio.FIRST_COMPLETED
    )
    for task in done:
      try:
        yield task.result()
        # Find the generator that produced this event and move it on.
        for i, original_task in enumerate(tasks):
          if task == original_task:
            new_task = asyncio.create_task(agent_runs[i].__anext__())
            tasks[i] = new_task
            pending_tasks.add(new_task)
            break  # stop iterating once found
      except StopAsyncIteration:
        continue
class ParallelAgent(BaseAgent):
  """A shell agent that run its sub-agents in parallel in isolated manner.
  This approach is beneficial for scenarios requiring multiple perspectives or
  attempts on a single task, such as:
  - Running different algorithms simultaneously.
  - Generating multiple responses for review by a subsequent evaluation agent.
  """
  @override
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    _set_branch_for_current_agent(self, ctx)
    agent_runs = [agent.run_async(ctx) for agent in self.sub_agents]
    async for event in _merge_agent_run(agent_runs):
      yield event
  @override
  async def _run_live_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    raise NotImplementedError("This is not supported yet for ParallelAgent.")
    yield  # AsyncGenerator requires having at least one yield statement
================================================
File: src/google/adk/agents/readonly_context.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from types import MappingProxyType
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from google.genai import types
  from .invocation_context import InvocationContext
class ReadonlyContext:
  def __init__(
      self,
      invocation_context: InvocationContext,
  ) -> None:
    self._invocation_context = invocation_context
  @property
  def user_content(self) -> Optional[types.Content]:
    """The user content that started this invocation. READONLY field."""
    return self._invocation_context.user_content
  @property
  def invocation_id(self) -> str:
    """The current invocation id."""
    return self._invocation_context.invocation_id
  @property
  def agent_name(self) -> str:
    """The name of the agent that is currently running."""
    return self._invocation_context.agent.name
  @property
  def state(self) -> MappingProxyType[str, Any]:
    """The state of the current session. READONLY field."""
    return MappingProxyType(self._invocation_context.session.state)
================================================
File: src/google/adk/agents/run_config.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from enum import Enum
import logging
import sys
from typing import Optional
from google.genai import types
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator
logger = logging.getLogger('google_adk.' + __name__)
class StreamingMode(Enum):
  NONE = None
  SSE = 'sse'
  BIDI = 'bidi'
class RunConfig(BaseModel):
  """Configs for runtime behavior of agents."""
  model_config = ConfigDict(
      extra='forbid',
  )
  """The pydantic model config."""
  speech_config: Optional[types.SpeechConfig] = None
  """Speech configuration for the live agent."""
  response_modalities: Optional[list[str]] = None
  """The output modalities. If not set, it's default to AUDIO."""
  save_input_blobs_as_artifacts: bool = False
  """Whether or not to save the input blobs as artifacts."""
  support_cfc: bool = False
  """
  Whether to support CFC (Compositional Function Calling). Only applicable for
  StreamingMode.SSE. If it's true. the LIVE API will be invoked. Since only LIVE
  API supports CFC
  .. warning::
      This feature is **experimental** and its API or behavior may change
      in future releases.
  """
  streaming_mode: StreamingMode = StreamingMode.NONE
  """Streaming mode, None or StreamingMode.SSE or StreamingMode.BIDI."""
  output_audio_transcription: Optional[types.AudioTranscriptionConfig] = None
  """Output transcription for live agents with audio response."""
  input_audio_transcription: Optional[types.AudioTranscriptionConfig] = None
  """Input transcription for live agents with audio input from user."""
  max_llm_calls: int = 500
  """
  A limit on the total number of llm calls for a given run.
  Valid Values:
    - More than 0 and less than sys.maxsize: The bound on the number of llm
      calls is enforced, if the value is set in this range.
    - Less than or equal to 0: This allows for unbounded number of llm calls.
  """
  @field_validator('max_llm_calls', mode='after')
  @classmethod
  def validate_max_llm_calls(cls, value: int) -> int:
    if value == sys.maxsize:
      raise ValueError(f'max_llm_calls should be less than {sys.maxsize}.')
    elif value <= 0:
      logger.warning(
          'max_llm_calls is less than or equal to 0. This will result in'
          ' no enforcement on total number of llm calls that will be made for a'
          ' run. This may not be ideal, as this could result in a never'
          ' ending communication between the model and the agent in certain'
          ' cases.',
      )
    return value
================================================
File: src/google/adk/agents/sequential_agent.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Sequential agent implementation."""
from __future__ import annotations
from typing import AsyncGenerator
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from ..events.event import Event
from .base_agent import BaseAgent
from .llm_agent import LlmAgent
class SequentialAgent(BaseAgent):
  """A shell agent that runs its sub-agents in sequence."""
  @override
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    for sub_agent in self.sub_agents:
      async for event in sub_agent.run_async(ctx):
        yield event
  @override
  async def _run_live_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    """Implementation for live SequentialAgent.
    Compared to the non-live case, live agents process a continuous stream of audio
    or video, so there is no way to tell if it's finished and should pass
    to the next agent or not. So we introduce a task_completed() function so the
    model can call this function to signal that it's finished the task and we
    can move on to the next agent.
    Args:
      ctx: The invocation context of the agent.
    """
    # There is no way to know if it's using live during init phase so we have to init it here
    for sub_agent in self.sub_agents:
      # add tool
      def task_completed():
        """
        Signals that the model has successfully completed the user's question
        or task.
        """
        return "Task completion signaled."
      if isinstance(sub_agent, LlmAgent):
        # Use function name to dedupe.
        if task_completed.__name__ not in sub_agent.tools:
          sub_agent.tools.append(task_completed)
          sub_agent.instruction += f"""If you finished the user's request
          according to its description, call the {task_completed.__name__} function
          to exit so the next agents can take over. When calling this function,
          do not generate any text other than the function call."""
    for sub_agent in self.sub_agents:
      async for event in sub_agent.run_live(ctx):
        yield event
================================================
File: src/google/adk/agents/transcription_entry.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Optional
from typing import Union
from google.genai import types
from pydantic import BaseModel
from pydantic import ConfigDict
class TranscriptionEntry(BaseModel):
  """Store the data that can be used for transcription."""
  model_config = ConfigDict(
      arbitrary_types_allowed=True,
      extra='forbid',
  )
  """The pydantic model config."""
  role: Optional[str] = None
  """The role that created this data, typically "user" or "model". For function 
  call, this is None."""
  data: Union[types.Blob, types.Content]
  """The data that can be used for transcription"""
================================================
File: src/google/adk/artifacts/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .base_artifact_service import BaseArtifactService
from .gcs_artifact_service import GcsArtifactService
from .in_memory_artifact_service import InMemoryArtifactService
__all__ = [
    'BaseArtifactService',
    'GcsArtifactService',
    'InMemoryArtifactService',
]
================================================
File: src/google/adk/artifacts/base_artifact_service.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from abc import ABC
from abc import abstractmethod
from typing import Optional
from google.genai import types
class BaseArtifactService(ABC):
  """Abstract base class for artifact services."""
  @abstractmethod
  async def save_artifact(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      artifact: types.Part,
  ) -> int:
    """Saves an artifact to the artifact service storage.
    The artifact is a file identified by the app name, user ID, session ID, and
    filename. After saving the artifact, a revision ID is returned to identify
    the artifact version.
    Args:
      app_name: The app name.
      user_id: The user ID.
      session_id: The session ID.
      filename: The filename of the artifact.
      artifact: The artifact to save.
    Returns:
      The revision ID. The first version of the artifact has a revision ID of 0.
      This is incremented by 1 after each successful save.
    """
  @abstractmethod
  async def load_artifact(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      version: Optional[int] = None,
  ) -> Optional[types.Part]:
    """Gets an artifact from the artifact service storage.
    The artifact is a file identified by the app name, user ID, session ID, and
    filename.
    Args:
      app_name: The app name.
      user_id: The user ID.
      session_id: The session ID.
      filename: The filename of the artifact.
        returned.
    Returns:
      The artifact or None if not found.
    """
  @abstractmethod
  async def list_artifact_keys(
      self, *, app_name: str, user_id: str, session_id: str
  ) -> list[str]:
    """Lists all the artifact filenames within a session.
    Args:
        app_name: The name of the application.
        user_id: The ID of the user.
        session_id: The ID of the session.
    Returns:
        A list of all artifact filenames within a session.
    """
  @abstractmethod
  async def delete_artifact(
      self, *, app_name: str, user_id: str, session_id: str, filename: str
  ) -> None:
    """Deletes an artifact.
    Args:
        app_name: The name of the application.
        user_id: The ID of the user.
        session_id: The ID of the session.
        filename: The name of the artifact file.
    """
  @abstractmethod
  async def list_versions(
      self, *, app_name: str, user_id: str, session_id: str, filename: str
  ) -> list[int]:
    """Lists all versions of an artifact.
    Args:
        app_name: The name of the application.
        user_id: The ID of the user.
        session_id: The ID of the session.
        filename: The name of the artifact file.
    Returns:
        A list of all available versions of the artifact.
    """
================================================
File: src/google/adk/artifacts/gcs_artifact_service.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""An artifact service implementation using Google Cloud Storage (GCS)."""
import logging
from typing import Optional
from google.cloud import storage
from google.genai import types
from typing_extensions import override
from .base_artifact_service import BaseArtifactService
logger = logging.getLogger("google_adk." + __name__)
class GcsArtifactService(BaseArtifactService):
  """An artifact service implementation using Google Cloud Storage (GCS)."""
  def __init__(self, bucket_name: str, **kwargs):
    """Initializes the GcsArtifactService.
    Args:
        bucket_name: The name of the bucket to use.
        **kwargs: Keyword arguments to pass to the Google Cloud Storage client.
    """
    self.bucket_name = bucket_name
    self.storage_client = storage.Client(**kwargs)
    self.bucket = self.storage_client.bucket(self.bucket_name)
  def _file_has_user_namespace(self, filename: str) -> bool:
    """Checks if the filename has a user namespace.
    Args:
        filename: The filename to check.
    Returns:
        True if the filename has a user namespace (starts with "user:"),
        False otherwise.
    """
    return filename.startswith("user:")
  def _get_blob_name(
      self,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      version: int,
  ) -> str:
    """Constructs the blob name in GCS.
    Args:
        app_name: The name of the application.
        user_id: The ID of the user.
        session_id: The ID of the session.
        filename: The name of the artifact file.
        version: The version of the artifact.
    Returns:
        The constructed blob name in GCS.
    """
    if self._file_has_user_namespace(filename):
      return f"{app_name}/{user_id}/user/{filename}/{version}"
    return f"{app_name}/{user_id}/{session_id}/{filename}/{version}"
  @override
  async def save_artifact(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      artifact: types.Part,
  ) -> int:
    versions = await self.list_versions(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        filename=filename,
    )
    version = 0 if not versions else max(versions) + 1
    blob_name = self._get_blob_name(
        app_name, user_id, session_id, filename, version
    )
    blob = self.bucket.blob(blob_name)
    blob.upload_from_string(
        data=artifact.inline_data.data,
        content_type=artifact.inline_data.mime_type,
    )
    return version
  @override
  async def load_artifact(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      version: Optional[int] = None,
  ) -> Optional[types.Part]:
    if version is None:
      versions = await self.list_versions(
          app_name=app_name,
          user_id=user_id,
          session_id=session_id,
          filename=filename,
      )
      if not versions:
        return None
      version = max(versions)
    blob_name = self._get_blob_name(
        app_name, user_id, session_id, filename, version
    )
    blob = self.bucket.blob(blob_name)
    artifact_bytes = blob.download_as_bytes()
    if not artifact_bytes:
      return None
    artifact = types.Part.from_bytes(
        data=artifact_bytes, mime_type=blob.content_type
    )
    return artifact
  @override
  async def list_artifact_keys(
      self, *, app_name: str, user_id: str, session_id: str
  ) -> list[str]:
    filenames = set()
    session_prefix = f"{app_name}/{user_id}/{session_id}/"
    session_blobs = self.storage_client.list_blobs(
        self.bucket, prefix=session_prefix
    )
    for blob in session_blobs:
      _, _, _, filename, _ = blob.name.split("/")
      filenames.add(filename)
    user_namespace_prefix = f"{app_name}/{user_id}/user/"
    user_namespace_blobs = self.storage_client.list_blobs(
        self.bucket, prefix=user_namespace_prefix
    )
    for blob in user_namespace_blobs:
      _, _, _, filename, _ = blob.name.split("/")
      filenames.add(filename)
    return sorted(list(filenames))
  @override
  async def delete_artifact(
      self, *, app_name: str, user_id: str, session_id: str, filename: str
  ) -> None:
    versions = await self.list_versions(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        filename=filename,
    )
    for version in versions:
      blob_name = self._get_blob_name(
          app_name, user_id, session_id, filename, version
      )
      blob = self.bucket.blob(blob_name)
      blob.delete()
    return
  @override
  async def list_versions(
      self, *, app_name: str, user_id: str, session_id: str, filename: str
  ) -> list[int]:
    prefix = self._get_blob_name(app_name, user_id, session_id, filename, "")
    blobs = self.storage_client.list_blobs(self.bucket, prefix=prefix)
    versions = []
    for blob in blobs:
      _, _, _, _, version = blob.name.split("/")
      versions.append(int(version))
    return versions
================================================
File: src/google/adk/artifacts/in_memory_artifact_service.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""An in-memory implementation of the artifact service."""
import logging
from typing import Optional
from google.genai import types
from pydantic import BaseModel
from pydantic import Field
from typing_extensions import override
from .base_artifact_service import BaseArtifactService
logger = logging.getLogger("google_adk." + __name__)
class InMemoryArtifactService(BaseArtifactService, BaseModel):
  """An in-memory implementation of the artifact service."""
  artifacts: dict[str, list[types.Part]] = Field(default_factory=dict)
  def _file_has_user_namespace(self, filename: str) -> bool:
    """Checks if the filename has a user namespace.
    Args:
        filename: The filename to check.
    Returns:
        True if the filename has a user namespace (starts with "user:"),
        False otherwise.
    """
    return filename.startswith("user:")
  def _artifact_path(
      self, app_name: str, user_id: str, session_id: str, filename: str
  ) -> str:
    """Constructs the artifact path.
    Args:
        app_name: The name of the application.
        user_id: The ID of the user.
        session_id: The ID of the session.
        filename: The name of the artifact file.
    Returns:
        The constructed artifact path.
    """
    if self._file_has_user_namespace(filename):
      return f"{app_name}/{user_id}/user/{filename}"
    return f"{app_name}/{user_id}/{session_id}/{filename}"
  @override
  async def save_artifact(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      artifact: types.Part,
  ) -> int:
    path = self._artifact_path(app_name, user_id, session_id, filename)
    if path not in self.artifacts:
      self.artifacts[path] = []
    version = len(self.artifacts[path])
    self.artifacts[path].append(artifact)
    return version
  @override
  async def load_artifact(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      filename: str,
      version: Optional[int] = None,
  ) -> Optional[types.Part]:
    path = self._artifact_path(app_name, user_id, session_id, filename)
    versions = self.artifacts.get(path)
    if not versions:
      return None
    if version is None:
      version = -1
    return versions[version]
  @override
  async def list_artifact_keys(
      self, *, app_name: str, user_id: str, session_id: str
  ) -> list[str]:
    session_prefix = f"{app_name}/{user_id}/{session_id}/"
    usernamespace_prefix = f"{app_name}/{user_id}/user/"
    filenames = []
    for path in self.artifacts:
      if path.startswith(session_prefix):
        filename = path.removeprefix(session_prefix)
        filenames.append(filename)
      elif path.startswith(usernamespace_prefix):
        filename = path.removeprefix(usernamespace_prefix)
        filenames.append(filename)
    return sorted(filenames)
  @override
  async def delete_artifact(
      self, *, app_name: str, user_id: str, session_id: str, filename: str
  ) -> None:
    path = self._artifact_path(app_name, user_id, session_id, filename)
    if not self.artifacts.get(path):
      return None
    self.artifacts.pop(path, None)
  @override
  async def list_versions(
      self, *, app_name: str, user_id: str, session_id: str, filename: str
  ) -> list[int]:
    path = self._artifact_path(app_name, user_id, session_id, filename)
    versions = self.artifacts.get(path)
    if not versions:
      return []
    return list(range(len(versions)))
================================================
File: src/google/adk/auth/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .auth_credential import AuthCredential
from .auth_credential import AuthCredentialTypes
from .auth_credential import OAuth2Auth
from .auth_handler import AuthHandler
from .auth_schemes import AuthScheme
from .auth_schemes import AuthSchemeType
from .auth_schemes import OpenIdConnectWithConfig
from .auth_tool import AuthConfig
================================================
File: src/google/adk/auth/auth_credential.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from pydantic import alias_generators
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
class BaseModelWithConfig(BaseModel):
  model_config = ConfigDict(
      extra="allow",
      alias_generator=alias_generators.to_camel,
      populate_by_name=True,
  )
  """The pydantic model config."""
class HttpCredentials(BaseModelWithConfig):
  """Represents the secret token value for HTTP authentication, like user name, password, oauth token, etc."""
  username: Optional[str] = None
  password: Optional[str] = None
  token: Optional[str] = None
  @classmethod
  def model_validate(cls, data: Dict[str, Any]) -> "HttpCredentials":
    return cls(
        username=data.get("username"),
        password=data.get("password"),
        token=data.get("token"),
    )
class HttpAuth(BaseModelWithConfig):
  """The credentials and metadata for HTTP authentication."""
  # The name of the HTTP Authorization scheme to be used in the Authorization
  # header as defined in RFC7235. The values used SHOULD be registered in the
  # IANA Authentication Scheme registry.
  # Examples: 'basic', 'bearer'
  scheme: str
  credentials: HttpCredentials
class OAuth2Auth(BaseModelWithConfig):
  """Represents credential value and its metadata for a OAuth2 credential."""
  client_id: Optional[str] = None
  client_secret: Optional[str] = None
  # tool or adk can generate the auth_uri with the state info thus client
  # can verify the state
  auth_uri: Optional[str] = None
  state: Optional[str] = None
  # tool or adk can decide the redirect_uri if they don't want client to decide
  redirect_uri: Optional[str] = None
  auth_response_uri: Optional[str] = None
  auth_code: Optional[str] = None
  access_token: Optional[str] = None
  refresh_token: Optional[str] = None
class ServiceAccountCredential(BaseModelWithConfig):
  """Represents Google Service Account configuration.
  Attributes:
    type: The type should be "service_account".
    project_id: The project ID.
    private_key_id: The ID of the private key.
    private_key: The private key.
    client_email: The client email.
    client_id: The client ID.
    auth_uri: The authorization URI.
    token_uri: The token URI.
    auth_provider_x509_cert_url: URL for auth provider's X.509 cert.
    client_x509_cert_url: URL for the client's X.509 cert.
    universe_domain: The universe domain.
  Example:
      config = ServiceAccountCredential(
          type_="service_account",
          project_id="your_project_id",
          private_key_id="your_private_key_id",
          client_email="...@....iam.gserviceaccount.com",
          client_id="your_client_id",
          auth_uri="https://accounts.google.com/o/oauth2/auth",
          token_uri="https://oauth2.googleapis.com/token",
          auth_provider_x509_cert_url="https://www.googleapis.com/oauth2/v1/certs",
          client_x509_cert_url="https://www.googleapis.com/robot/v1/metadata/x509/...",
          universe_domain="googleapis.com"
      )
      config = ServiceAccountConfig.model_construct(**{
          ...service account config dict
      })
  """
  type_: str = Field("", alias="type")
  project_id: str
  private_key_id: str
  private_key: str
  client_email: str
  client_id: str
  auth_uri: str
  token_uri: str
  auth_provider_x509_cert_url: str
  client_x509_cert_url: str
  universe_domain: str
class ServiceAccount(BaseModelWithConfig):
  """Represents Google Service Account configuration."""
  service_account_credential: Optional[ServiceAccountCredential] = None
  scopes: List[str]
  use_default_credential: Optional[bool] = False
class AuthCredentialTypes(str, Enum):
  """Represents the type of authentication credential."""
  # API Key credential:
  # https://swagger.io/docs/specification/v3_0/authentication/api-keys/
  API_KEY = "apiKey"
  # Credentials for HTTP Auth schemes:
  # https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml
  HTTP = "http"
  # OAuth2 credentials:
  # https://swagger.io/docs/specification/v3_0/authentication/oauth2/
  OAUTH2 = "oauth2"
  # OpenID Connect credentials:
  # https://swagger.io/docs/specification/v3_0/authentication/openid-connect-discovery/
  OPEN_ID_CONNECT = "openIdConnect"
  # Service Account credentials:
  # https://cloud.google.com/iam/docs/service-account-creds
  SERVICE_ACCOUNT = "serviceAccount"
class AuthCredential(BaseModelWithConfig):
  """Data class representing an authentication credential.
  To exchange for the actual credential, please use
  CredentialExchanger.exchange_credential().
  Examples: API Key Auth
  AuthCredential(
      auth_type=AuthCredentialTypes.API_KEY,
      api_key="1234",
  )
  Example: HTTP Auth
  AuthCredential(
      auth_type=AuthCredentialTypes.HTTP,
      http=HttpAuth(
          scheme="basic",
          credentials=HttpCredentials(username="user", password="password"),
      ),
  )
  Example: OAuth2 Bearer Token in HTTP Header
  AuthCredential(
      auth_type=AuthCredentialTypes.HTTP,
      http=HttpAuth(
          scheme="bearer",
          credentials=HttpCredentials(token="eyAkaknabna...."),
      ),
  )
  Example: OAuth2 Auth with Authorization Code Flow
  AuthCredential(
      auth_type=AuthCredentialTypes.OAUTH2,
      oauth2=OAuth2Auth(
          client_id="1234",
          client_secret="secret",
      ),
  )
  Example: OpenID Connect Auth
  AuthCredential(
      auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
      oauth2=OAuth2Auth(
          client_id="1234",
          client_secret="secret",
          redirect_uri="https://example.com",
          scopes=["scope1", "scope2"],
      ),
  )
  Example: Auth with resource reference
  AuthCredential(
      auth_type=AuthCredentialTypes.API_KEY,
      resource_ref="projects/1234/locations/us-central1/resources/resource1",
  )
  """
  auth_type: AuthCredentialTypes
  # Resource reference for the credential.
  # This will be supported in the future.
  resource_ref: Optional[str] = None
  api_key: Optional[str] = None
  http: Optional[HttpAuth] = None
  service_account: Optional[ServiceAccount] = None
  oauth2: Optional[OAuth2Auth] = None
================================================
File: src/google/adk/auth/auth_handler.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import SecurityBase
from .auth_credential import AuthCredential
from .auth_credential import AuthCredentialTypes
from .auth_credential import OAuth2Auth
from .auth_schemes import AuthSchemeType
from .auth_schemes import OAuthGrantType
from .auth_schemes import OpenIdConnectWithConfig
from .auth_tool import AuthConfig
if TYPE_CHECKING:
  from ..sessions.state import State
try:
  from authlib.integrations.requests_client import OAuth2Session
  SUPPORT_TOKEN_EXCHANGE = True
except ImportError:
  SUPPORT_TOKEN_EXCHANGE = False
class AuthHandler:
  def __init__(self, auth_config: AuthConfig):
    self.auth_config = auth_config
  def exchange_auth_token(
      self,
  ) -> AuthCredential:
    """Generates an auth token from the authorization response.
    Returns:
        An AuthCredential object containing the access token.
    Raises:
        ValueError: If the token endpoint is not configured in the auth
            scheme.
        AuthCredentialMissingError: If the access token cannot be retrieved
            from the token endpoint.
    """
    auth_scheme = self.auth_config.auth_scheme
    auth_credential = self.auth_config.exchanged_auth_credential
    if not SUPPORT_TOKEN_EXCHANGE:
      return auth_credential
    if isinstance(auth_scheme, OpenIdConnectWithConfig):
      if not hasattr(auth_scheme, "token_endpoint"):
        return self.auth_config.exchanged_auth_credential
      token_endpoint = auth_scheme.token_endpoint
      scopes = auth_scheme.scopes
    elif isinstance(auth_scheme, OAuth2):
      if (
          not auth_scheme.flows.authorizationCode
          or not auth_scheme.flows.authorizationCode.tokenUrl
      ):
        return self.auth_config.exchanged_auth_credential
      token_endpoint = auth_scheme.flows.authorizationCode.tokenUrl
      scopes = list(auth_scheme.flows.authorizationCode.scopes.keys())
    else:
      return self.auth_config.exchanged_auth_credential
    if (
        not auth_credential
        or not auth_credential.oauth2
        or not auth_credential.oauth2.client_id
        or not auth_credential.oauth2.client_secret
        or auth_credential.oauth2.access_token
        or auth_credential.oauth2.refresh_token
    ):
      return self.auth_config.exchanged_auth_credential
    client = OAuth2Session(
        auth_credential.oauth2.client_id,
        auth_credential.oauth2.client_secret,
        scope=" ".join(scopes),
        redirect_uri=auth_credential.oauth2.redirect_uri,
        state=auth_credential.oauth2.state,
    )
    tokens = client.fetch_token(
        token_endpoint,
        authorization_response=auth_credential.oauth2.auth_response_uri,
        code=auth_credential.oauth2.auth_code,
        grant_type=OAuthGrantType.AUTHORIZATION_CODE,
    )
    updated_credential = AuthCredential(
        auth_type=AuthCredentialTypes.OAUTH2,
        oauth2=OAuth2Auth(
            access_token=tokens.get("access_token"),
            refresh_token=tokens.get("refresh_token"),
        ),
    )
    return updated_credential
  def parse_and_store_auth_response(self, state: State) -> None:
    credential_key = self.get_credential_key()
    state[credential_key] = self.auth_config.exchanged_auth_credential
    if not isinstance(
        self.auth_config.auth_scheme, SecurityBase
    ) or self.auth_config.auth_scheme.type_ not in (
        AuthSchemeType.oauth2,
        AuthSchemeType.openIdConnect,
    ):
      return
    state[credential_key] = self.exchange_auth_token()
  def _validate(self) -> None:
    if not self.auth_scheme:
      raise ValueError("auth_scheme is empty.")
  def get_auth_response(self, state: State) -> AuthCredential:
    credential_key = self.get_credential_key()
    return state.get(credential_key, None)
  def generate_auth_request(self) -> AuthConfig:
    if not isinstance(
        self.auth_config.auth_scheme, SecurityBase
    ) or self.auth_config.auth_scheme.type_ not in (
        AuthSchemeType.oauth2,
        AuthSchemeType.openIdConnect,
    ):
      return self.auth_config.model_copy(deep=True)
    # auth_uri already in exchanged credential
    if (
        self.auth_config.exchanged_auth_credential
        and self.auth_config.exchanged_auth_credential.oauth2
        and self.auth_config.exchanged_auth_credential.oauth2.auth_uri
    ):
      return self.auth_config.model_copy(deep=True)
    # Check if raw_auth_credential exists
    if not self.auth_config.raw_auth_credential:
      raise ValueError(
          f"Auth Scheme {self.auth_config.auth_scheme.type_} requires"
          " auth_credential."
      )
    # Check if oauth2 exists in raw_auth_credential
    if not self.auth_config.raw_auth_credential.oauth2:
      raise ValueError(
          f"Auth Scheme {self.auth_config.auth_scheme.type_} requires oauth2 in"
          " auth_credential."
      )
    # auth_uri in raw credential
    if self.auth_config.raw_auth_credential.oauth2.auth_uri:
      return AuthConfig(
          auth_scheme=self.auth_config.auth_scheme,
          raw_auth_credential=self.auth_config.raw_auth_credential,
          exchanged_auth_credential=self.auth_config.raw_auth_credential.model_copy(
              deep=True
          ),
      )
    # Check for client_id and client_secret
    if (
        not self.auth_config.raw_auth_credential.oauth2.client_id
        or not self.auth_config.raw_auth_credential.oauth2.client_secret
    ):
      raise ValueError(
          f"Auth Scheme {self.auth_config.auth_scheme.type_} requires both"
          " client_id and client_secret in auth_credential.oauth2."
      )
    # Generate new auth URI
    exchanged_credential = self.generate_auth_uri()
    return AuthConfig(
        auth_scheme=self.auth_config.auth_scheme,
        raw_auth_credential=self.auth_config.raw_auth_credential,
        exchanged_auth_credential=exchanged_credential,
    )
  def get_credential_key(self) -> str:
    """Generates a unique key for the given auth scheme and credential."""
    auth_scheme = self.auth_config.auth_scheme
    auth_credential = self.auth_config.raw_auth_credential
    if auth_scheme.model_extra:
      auth_scheme = auth_scheme.model_copy(deep=True)
      auth_scheme.model_extra.clear()
    scheme_name = (
        f"{auth_scheme.type_.name}_{hash(auth_scheme.model_dump_json())}"
        if auth_scheme
        else ""
    )
    if auth_credential.model_extra:
      auth_credential = auth_credential.model_copy(deep=True)
      auth_credential.model_extra.clear()
    credential_name = (
        f"{auth_credential.auth_type.value}_{hash(auth_credential.model_dump_json())}"
        if auth_credential
        else ""
    )
    return f"temp:adk_{scheme_name}_{credential_name}"
  def generate_auth_uri(
      self,
  ) -> AuthCredential:
    """Generates an response containing the auth uri for user to sign in.
    Returns:
        An AuthCredential object containing the auth URI and state.
    Raises:
        ValueError: If the authorization endpoint is not configured in the auth
            scheme.
    """
    auth_scheme = self.auth_config.auth_scheme
    auth_credential = self.auth_config.raw_auth_credential
    if isinstance(auth_scheme, OpenIdConnectWithConfig):
      authorization_endpoint = auth_scheme.authorization_endpoint
      scopes = auth_scheme.scopes
    else:
      authorization_endpoint = (
          auth_scheme.flows.implicit
          and auth_scheme.flows.implicit.authorizationUrl
          or auth_scheme.flows.authorizationCode
          and auth_scheme.flows.authorizationCode.authorizationUrl
          or auth_scheme.flows.clientCredentials
          and auth_scheme.flows.clientCredentials.tokenUrl
          or auth_scheme.flows.password
          and auth_scheme.flows.password.tokenUrl
      )
      scopes = (
          auth_scheme.flows.implicit
          and auth_scheme.flows.implicit.scopes
          or auth_scheme.flows.authorizationCode
          and auth_scheme.flows.authorizationCode.scopes
          or auth_scheme.flows.clientCredentials
          and auth_scheme.flows.clientCredentials.scopes
          or auth_scheme.flows.password
          and auth_scheme.flows.password.scopes
      )
      scopes = list(scopes.keys())
    client = OAuth2Session(
        auth_credential.oauth2.client_id,
        auth_credential.oauth2.client_secret,
        scope=" ".join(scopes),
        redirect_uri=auth_credential.oauth2.redirect_uri,
    )
    uri, state = client.create_authorization_url(
        url=authorization_endpoint, access_type="offline", prompt="consent"
    )
    exchanged_auth_credential = auth_credential.model_copy(deep=True)
    exchanged_auth_credential.oauth2.auth_uri = uri
    exchanged_auth_credential.oauth2.state = state
    return exchanged_auth_credential
================================================
File: src/google/adk/auth/auth_preprocessor.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import AsyncGenerator
from typing import TYPE_CHECKING
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from ..agents.readonly_context import ReadonlyContext
from ..events.event import Event
from ..flows.llm_flows import functions
from ..flows.llm_flows._base_llm_processor import BaseLlmRequestProcessor
from ..flows.llm_flows.functions import REQUEST_EUC_FUNCTION_CALL_NAME
from ..models.llm_request import LlmRequest
from .auth_handler import AuthHandler
from .auth_tool import AuthConfig
from .auth_tool import AuthToolArguments
if TYPE_CHECKING:
  from ..agents.llm_agent import LlmAgent
class _AuthLlmRequestProcessor(BaseLlmRequestProcessor):
  """Handles auth information to build the LLM request."""
  @override
  async def run_async(
      self, invocation_context: InvocationContext, llm_request: LlmRequest
  ) -> AsyncGenerator[Event, None]:
    from ..agents.llm_agent import LlmAgent
    agent = invocation_context.agent
    if not isinstance(agent, LlmAgent):
      return
    events = invocation_context.session.events
    if not events:
      return
    request_euc_function_call_ids = set()
    for k in range(len(events) - 1, -1, -1):
      event = events[k]
      # look for first event authored by user
      if not event.author or event.author != 'user':
        continue
      responses = event.get_function_responses()
      if not responses:
        return
      for function_call_response in responses:
        if function_call_response.name != REQUEST_EUC_FUNCTION_CALL_NAME:
          continue
        # found the function call response for the system long running request euc
        # function call
        request_euc_function_call_ids.add(function_call_response.id)
        auth_config = AuthConfig.model_validate(function_call_response.response)
        AuthHandler(auth_config=auth_config).parse_and_store_auth_response(
            state=invocation_context.session.state
        )
      break
    if not request_euc_function_call_ids:
      return
    for i in range(len(events) - 2, -1, -1):
      event = events[i]
      # looking for the system long running request euc function call
      function_calls = event.get_function_calls()
      if not function_calls:
        continue
      tools_to_resume = set()
      for function_call in function_calls:
        if function_call.id not in request_euc_function_call_ids:
          continue
        args = AuthToolArguments.model_validate(function_call.args)
        tools_to_resume.add(args.function_call_id)
      if not tools_to_resume:
        continue
      # found the the system long running request euc function call
      # looking for original function call that requests euc
      for j in range(i - 1, -1, -1):
        event = events[j]
        function_calls = event.get_function_calls()
        if not function_calls:
          continue
        if any([
            function_call.id in tools_to_resume
            for function_call in function_calls
        ]):
          if function_response_event := await functions.handle_function_calls_async(
              invocation_context,
              event,
              {
                  tool.name: tool
                  for tool in await agent.canonical_tools(
                      ReadonlyContext(invocation_context)
                  )
              },
              # there could be parallel function calls that require auth
              # auth response would be a dict keyed by function call id
              tools_to_resume,
          ):
            yield function_response_event
          return
      return
request_processor = _AuthLlmRequestProcessor()
================================================
File: src/google/adk/auth/auth_schemes.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from enum import Enum
from typing import List
from typing import Optional
from typing import Union
from fastapi.openapi.models import OAuthFlows
from fastapi.openapi.models import SecurityBase
from fastapi.openapi.models import SecurityScheme
from fastapi.openapi.models import SecuritySchemeType
from pydantic import Field
class OpenIdConnectWithConfig(SecurityBase):
  type_: SecuritySchemeType = Field(
      default=SecuritySchemeType.openIdConnect, alias="type"
  )
  authorization_endpoint: str
  token_endpoint: str
  userinfo_endpoint: Optional[str] = None
  revocation_endpoint: Optional[str] = None
  token_endpoint_auth_methods_supported: Optional[List[str]] = None
  grant_types_supported: Optional[List[str]] = None
  scopes: Optional[List[str]] = None
# AuthSchemes contains SecuritySchemes from OpenAPI 3.0 and an extra flattened OpenIdConnectWithConfig.
AuthScheme = Union[SecurityScheme, OpenIdConnectWithConfig]
class OAuthGrantType(str, Enum):
  """Represents the OAuth2 flow (or grant type)."""
  CLIENT_CREDENTIALS = "client_credentials"
  AUTHORIZATION_CODE = "authorization_code"
  PASSWORD = "password"
  @staticmethod
  def from_flow(flow: OAuthFlows) -> "OAuthGrantType":
    """Converts an OAuthFlows object to a OAuthGrantType."""
    if flow.clientCredentials:
      return OAuthGrantType.CLIENT_CREDENTIALS
    if flow.authorizationCode:
      return OAuthGrantType.AUTHORIZATION_CODE
    if flow.implicit:
    if flow.password:
      return OAuthGrantType.PASSWORD
    return None
# AuthSchemeType re-exports SecuritySchemeType from OpenAPI 3.0.
AuthSchemeType = SecuritySchemeType
================================================
File: src/google/adk/auth/auth_tool.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .auth_credential import AuthCredential
from .auth_credential import BaseModelWithConfig
from .auth_schemes import AuthScheme
class AuthConfig(BaseModelWithConfig):
  """The auth config sent by tool asking client to collect auth credentials and
  adk and client will help to fill in the response
  """
  auth_scheme: AuthScheme
  """The auth scheme used to collect credentials"""
  raw_auth_credential: AuthCredential = None
  """The raw auth credential used to collect credentials. The raw auth
  credentials are used in some auth scheme that needs to exchange auth
  credentials. e.g. OAuth2 and OIDC. For other auth scheme, it could be None.
  """
  exchanged_auth_credential: AuthCredential = None
  """The exchanged auth credential used to collect credentials. adk and client
  will work together to fill it. For those auth scheme that doesn't need to
  exchange auth credentials, e.g. API key, service account etc. It's filled by
  client directly. For those auth scheme that need to exchange auth credentials,
  e.g. OAuth2 and OIDC, it's first filled by adk. If the raw credentials
  passed by tool only has client id and client credential, adk will help to
  generate the corresponding authorization uri and state and store the processed
  credential in this field. If the raw credentials passed by tool already has
  authorization uri, state, etc. then it's copied to this field. Client will use
  this field to guide the user through the OAuth2 flow and fill auth response in
  this field"""
class AuthToolArguments(BaseModelWithConfig):
  """the arguments for the special long running function tool that is used to
  request end user credentials.
  """
  function_call_id: str
  auth_config: AuthConfig
================================================
File: src/google/adk/cli/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .cli_tools_click import main
================================================
File: src/google/adk/cli/__main__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .cli_tools_click import main
if __name__ == '__main__':
  main()
================================================
File: src/google/adk/cli/agent_graph.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import logging
from typing import Union
import graphviz
from ..agents import BaseAgent
from ..agents.llm_agent import LlmAgent
from ..tools.agent_tool import AgentTool
from ..tools.base_tool import BaseTool
from ..tools.function_tool import FunctionTool
logger = logging.getLogger('google_adk.' + __name__)
try:
  from ..tools.retrieval.base_retrieval_tool import BaseRetrievalTool
except ModuleNotFoundError:
  retrieval_tool_module_loaded = False
else:
  retrieval_tool_module_loaded = True
async def build_graph(graph, agent: BaseAgent, highlight_pairs):
  dark_green = '#0F5223'
  light_green = '#69CB87'
  light_gray = '#cccccc'
  def get_node_name(tool_or_agent: Union[BaseAgent, BaseTool]):
    if isinstance(tool_or_agent, BaseAgent):
      return tool_or_agent.name
    elif isinstance(tool_or_agent, BaseTool):
      return tool_or_agent.name
    else:
      raise ValueError(f'Unsupported tool type: {tool_or_agent}')
  def get_node_caption(tool_or_agent: Union[BaseAgent, BaseTool]):
    if isinstance(tool_or_agent, BaseAgent):
      return '🤖 ' + tool_or_agent.name
    elif retrieval_tool_module_loaded and isinstance(
        tool_or_agent, BaseRetrievalTool
    ):
      return '🔎 ' + tool_or_agent.name
    elif isinstance(tool_or_agent, FunctionTool):
      return '🔧 ' + tool_or_agent.name
    elif isinstance(tool_or_agent, AgentTool):
      return '🤖 ' + tool_or_agent.name
    elif isinstance(tool_or_agent, BaseTool):
      return '🔧 ' + tool_or_agent.name
    else:
      logger.warning(
          'Unsupported tool, type: %s, obj: %s',
          type(tool_or_agent),
          tool_or_agent,
      )
      return f'❓ Unsupported tool type: {type(tool_or_agent)}'
  def get_node_shape(tool_or_agent: Union[BaseAgent, BaseTool]):
    if isinstance(tool_or_agent, BaseAgent):
      return 'ellipse'
    elif retrieval_tool_module_loaded and isinstance(
        tool_or_agent, BaseRetrievalTool
    ):
      return 'cylinder'
    elif isinstance(tool_or_agent, FunctionTool):
      return 'box'
    elif isinstance(tool_or_agent, BaseTool):
      return 'box'
    else:
      logger.warning(
          'Unsupported tool, type: %s, obj: %s',
          type(tool_or_agent),
          tool_or_agent,
      )
      return 'cylinder'
  def draw_node(tool_or_agent: Union[BaseAgent, BaseTool]):
    name = get_node_name(tool_or_agent)
    shape = get_node_shape(tool_or_agent)
    caption = get_node_caption(tool_or_agent)
    if highlight_pairs:
      for highlight_tuple in highlight_pairs:
        if name in highlight_tuple:
          graph.node(
              name,
              caption,
              style='filled,rounded',
              fillcolor=dark_green,
              color=dark_green,
              shape=shape,
              fontcolor=light_gray,
          )
          return
    # if not in highlight, draw non-highliht node
    graph.node(
        name,
        caption,
        shape=shape,
        style='rounded',
        color=light_gray,
        fontcolor=light_gray,
    )
  def draw_edge(from_name, to_name):
    if highlight_pairs:
      for highlight_from, highlight_to in highlight_pairs:
        if from_name == highlight_from and to_name == highlight_to:
          graph.edge(from_name, to_name, color=light_green)
          return
        elif from_name == highlight_to and to_name == highlight_from:
          graph.edge(from_name, to_name, color=light_green, dir='back')
          return
    # if no need to highlight, color gray
    graph.edge(from_name, to_name, arrowhead='none', color=light_gray)
  draw_node(agent)
  for sub_agent in agent.sub_agents:
    await build_graph(graph, sub_agent, highlight_pairs)
    draw_edge(agent.name, sub_agent.name)
  if isinstance(agent, LlmAgent):
    for tool in await agent.canonical_tools():
      draw_node(tool)
      draw_edge(agent.name, get_node_name(tool))
async def get_agent_graph(root_agent, highlights_pairs, image=False):
  print('build graph')
  graph = graphviz.Digraph(graph_attr={'rankdir': 'LR', 'bgcolor': '#333537'})
  await build_graph(graph, root_agent, highlights_pairs)
  if image:
    return graph.pipe(format='png')
  else:
    return graph
================================================
File: src/google/adk/cli/cli.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from datetime import datetime
from typing import Optional
import click
from google.genai import types
from pydantic import BaseModel
from ..agents.llm_agent import LlmAgent
from ..artifacts import BaseArtifactService
from ..artifacts import InMemoryArtifactService
from ..runners import Runner
from ..sessions.base_session_service import BaseSessionService
from ..sessions.in_memory_session_service import InMemorySessionService
from ..sessions.session import Session
from .utils import envs
from .utils.agent_loader import AgentLoader
class InputFile(BaseModel):
  state: dict[str, object]
  queries: list[str]
async def run_input_file(
    app_name: str,
    user_id: str,
    root_agent: LlmAgent,
    artifact_service: BaseArtifactService,
    session_service: BaseSessionService,
    input_path: str,
) -> Session:
  runner = Runner(
      app_name=app_name,
      agent=root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  with open(input_path, 'r', encoding='utf-8') as f:
    input_file = InputFile.model_validate_json(f.read())
  input_file.state['_time'] = datetime.now()
  session = await session_service.create_session(
      app_name=app_name, user_id=user_id, state=input_file.state
  )
  for query in input_file.queries:
    click.echo(f'[user]: {query}')
    content = types.Content(role='user', parts=[types.Part(text=query)])
    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=content
    ):
      if event.content and event.content.parts:
        if text := ''.join(part.text or '' for part in event.content.parts):
          click.echo(f'[{event.author}]: {text}')
  return session
async def run_interactively(
    root_agent: LlmAgent,
    artifact_service: BaseArtifactService,
    session: Session,
    session_service: BaseSessionService,
) -> None:
  runner = Runner(
      app_name=session.app_name,
      agent=root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  while True:
    query = input('[user]: ')
    if not query or not query.strip():
      continue
    if query == 'exit':
      break
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=types.Content(role='user', parts=[types.Part(text=query)]),
    ):
      if event.content and event.content.parts:
        if text := ''.join(part.text or '' for part in event.content.parts):
          click.echo(f'[{event.author}]: {text}')
  await runner.close()
async def run_cli(
    *,
    agent_parent_dir: str,
    agent_folder_name: str,
    input_file: Optional[str] = None,
    saved_session_file: Optional[str] = None,
    save_session: bool,
    session_id: Optional[str] = None,
) -> None:
  """Runs an interactive CLI for a certain agent.
  Args:
    agent_parent_dir: str, the absolute path of the parent folder of the agent
      folder.
    agent_folder_name: str, the name of the agent folder.
    input_file: Optional[str], the absolute path to the json file that contains
      the initial session state and user queries, exclusive with
      saved_session_file.
    saved_session_file: Optional[str], the absolute path to the json file that
      contains a previously saved session, exclusive with input_file.
    save_session: bool, whether to save the session on exit.
    session_id: Optional[str], the session ID to save the session to on exit.
  """
  artifact_service = InMemoryArtifactService()
  session_service = InMemorySessionService()
  session = await session_service.create_session(
      app_name=agent_folder_name, user_id=user_id
  )
  root_agent = AgentLoader(agents_dir=agent_parent_dir).load_agent(
      agent_folder_name
  )
  envs.load_dotenv_for_agent(agent_folder_name, agent_parent_dir)
  if input_file:
    session = await run_input_file(
        app_name=agent_folder_name,
        user_id=user_id,
        root_agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
        input_path=input_file,
    )
  elif saved_session_file:
    with open(saved_session_file, 'r', encoding='utf-8') as f:
      loaded_session = Session.model_validate_json(f.read())
    if loaded_session:
      for event in loaded_session.events:
        await session_service.append_event(session, event)
        content = event.content
        if not content or not content.parts or not content.parts[0].text:
          continue
        if event.author == 'user':
          click.echo(f'[user]: {content.parts[0].text}')
        else:
          click.echo(f'[{event.author}]: {content.parts[0].text}')
    await run_interactively(
        root_agent,
        artifact_service,
        session,
        session_service,
    )
  else:
    click.echo(f'Running agent {root_agent.name}, type exit to exit.')
    await run_interactively(
        root_agent,
        artifact_service,
        session,
        session_service,
    )
  if save_session:
    session_id = session_id or input('Session ID to save: ')
    session_path = (
        f'{agent_parent_dir}/{agent_folder_name}/{session_id}.session.json'
    )
    # Fetch the session again to get all the details.
    session = await session_service.get_session(
        app_name=session.app_name,
        user_id=session.user_id,
        session_id=session.id,
    )
    with open(session_path, 'w', encoding='utf-8') as f:
      f.write(session.model_dump_json(indent=2, exclude_none=True))
    print('Session saved to', session_path)
================================================
File: src/google/adk/cli/cli_create.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import subprocess
from typing import Optional
from typing import Tuple
import click
_INIT_PY_TEMPLATE = """\
from . import agent
"""
_AGENT_PY_TEMPLATE = """\
from google.adk.agents import Agent
root_agent = Agent(
    model='{model_name}',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
"""
_GOOGLE_API_MSG = """
Don't have API Key? Create one in AI Studio: https://aistudio.google.com/apikey
"""
_GOOGLE_CLOUD_SETUP_MSG = """
You need an existing Google Cloud account and project, check out this link for details:
"""
_OTHER_MODEL_MSG = """
Please see below guide to configure other models:
"""
_SUCCESS_MSG = """
Agent created in {agent_folder}:
- .env
- __init__.py
- agent.py
"""
def _get_gcp_project_from_gcloud() -> str:
  """Uses gcloud to get default project."""
  try:
    result = subprocess.run(
        ["gcloud", "config", "get-value", "project"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
  except (subprocess.CalledProcessError, FileNotFoundError):
    return ""
def _get_gcp_region_from_gcloud() -> str:
  """Uses gcloud to get default region."""
  try:
    result = subprocess.run(
        ["gcloud", "config", "get-value", "compute/region"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
  except (subprocess.CalledProcessError, FileNotFoundError):
    return ""
def _prompt_str(
    prompt_prefix: str,
    *,
    prior_msg: Optional[str] = None,
    default_value: Optional[str] = None,
) -> str:
  if prior_msg:
    click.secho(prior_msg, fg="green")
  while True:
    value: str = click.prompt(
        prompt_prefix, default=default_value or None, type=str
    )
    if value and value.strip():
      return value.strip()
def _prompt_for_google_cloud(
    google_cloud_project: Optional[str],
) -> str:
  """Prompts user for Google Cloud project ID."""
  google_cloud_project = (
      google_cloud_project
      or _get_gcp_project_from_gcloud()
  )
  google_cloud_project = _prompt_str(
      "Enter Google Cloud project ID", default_value=google_cloud_project
  )
  return google_cloud_project
def _prompt_for_google_cloud_region(
    google_cloud_region: Optional[str],
) -> str:
  """Prompts user for Google Cloud region."""
  google_cloud_region = (
      google_cloud_region
      or os.environ.get("GOOGLE_CLOUD_LOCATION", None)
      or _get_gcp_region_from_gcloud()
  )
  google_cloud_region = _prompt_str(
      "Enter Google Cloud region",
      default_value=google_cloud_region or "us-central1",
  )
  return google_cloud_region
def _prompt_for_google_api_key(
    google_api_key: Optional[str],
) -> str:
  """Prompts user for Google API key."""
  google_api_key = google_api_key or os.environ.get("GOOGLE_API_KEY", None)
  google_api_key = _prompt_str(
      "Enter Google API key",
      prior_msg=_GOOGLE_API_MSG,
      default_value=google_api_key,
  )
  return google_api_key
def _generate_files(
    agent_folder: str,
    *,
    google_api_key: Optional[str] = None,
    google_cloud_project: Optional[str] = None,
    google_cloud_region: Optional[str] = None,
    model: Optional[str] = None,
):
  """Generates a folder name for the agent."""
  os.makedirs(agent_folder, exist_ok=True)
  dotenv_file_path = os.path.join(agent_folder, ".env")
  init_file_path = os.path.join(agent_folder, "__init__.py")
  agent_file_path = os.path.join(agent_folder, "agent.py")
  with open(dotenv_file_path, "w", encoding="utf-8") as f:
    lines = []
    if google_api_key:
      lines.append("GOOGLE_GENAI_USE_VERTEXAI=0")
    elif google_cloud_project and google_cloud_region:
      lines.append("GOOGLE_GENAI_USE_VERTEXAI=1")
    if google_api_key:
      lines.append(f"GOOGLE_API_KEY={google_api_key}")
    if google_cloud_project:
    if google_cloud_region:
      lines.append(f"GOOGLE_CLOUD_LOCATION={google_cloud_region}")
    f.write("\n".join(lines))
  with open(init_file_path, "w", encoding="utf-8") as f:
    f.write(_INIT_PY_TEMPLATE)
  with open(agent_file_path, "w", encoding="utf-8") as f:
    f.write(_AGENT_PY_TEMPLATE.format(model_name=model))
  click.secho(
      _SUCCESS_MSG.format(agent_folder=agent_folder),
      fg="green",
  )
def _prompt_for_model() -> str:
  model_choice = click.prompt(
      """\
Choose a model for the root agent:
1. gemini-2.0-flash-001
2. Other models (fill later)
Choose model""",
      type=click.Choice(["1", "2"]),
  )
  if model_choice == "1":
    return "gemini-2.0-flash-001"
  else:
    click.secho(_OTHER_MODEL_MSG, fg="green")
    return "<FILL_IN_MODEL>"
def _prompt_to_choose_backend(
    google_api_key: Optional[str],
    google_cloud_project: Optional[str],
    google_cloud_region: Optional[str],
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
  """Prompts user to choose backend.
  Returns:
    A tuple of (google_api_key, google_cloud_project, google_cloud_region).
  """
  backend_choice = click.prompt(
      "1. Google AI\n2. Vertex AI\nChoose a backend",
      type=click.Choice(["1", "2"]),
  )
  if backend_choice == "1":
    google_api_key = _prompt_for_google_api_key(google_api_key)
  elif backend_choice == "2":
    click.secho(_GOOGLE_CLOUD_SETUP_MSG, fg="green")
    google_cloud_project = _prompt_for_google_cloud(google_cloud_project)
    google_cloud_region = _prompt_for_google_cloud_region(google_cloud_region)
  return google_api_key, google_cloud_project, google_cloud_region
def run_cmd(
    agent_name: str,
    *,
    model: Optional[str],
    google_api_key: Optional[str],
    google_cloud_project: Optional[str],
    google_cloud_region: Optional[str],
):
  """Runs `adk create` command to create agent template.
  Args:
    agent_name: str, The name of the agent.
    google_api_key: Optional[str], The Google API key for using Google AI as
      backend.
    google_cloud_project: Optional[str], The Google Cloud project for using
      VertexAI as backend.
    google_cloud_region: Optional[str], The Google Cloud region for using
      VertexAI as backend.
  """
  agent_folder = os.path.join(os.getcwd(), agent_name)
  # check folder doesn't exist or it's empty. Otherwise, throw
  if os.path.exists(agent_folder) and os.listdir(agent_folder):
    # Prompt user whether to override existing files using click
    if not click.confirm(
        f"Non-empty folder already exist: '{agent_folder}'\n"
        "Override existing content?",
        default=False,
    ):
      raise click.Abort()
  if not model:
    model = _prompt_for_model()
  if not google_api_key and not (google_cloud_project and google_cloud_region):
    if model.startswith("gemini"):
      google_api_key, google_cloud_project, google_cloud_region = (
          _prompt_to_choose_backend(
              google_api_key, google_cloud_project, google_cloud_region
          )
      )
  _generate_files(
      agent_folder,
      google_api_key=google_api_key,
      google_cloud_project=google_cloud_project,
      google_cloud_region=google_cloud_region,
      model=model,
  )
================================================
File: src/google/adk/cli/cli_deploy.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import os
import shutil
import subprocess
from typing import Optional
import click
_DOCKERFILE_TEMPLATE = """
FROM python:3.11-slim
WORKDIR /app
# Create a non-root user
RUN adduser --disabled-password --gecos "" myuser
# Change ownership of /app to myuser
RUN chown -R myuser:myuser /app
# Switch to the non-root user
USER myuser
# Set up environment variables - Start
ENV PATH="/home/myuser/.local/bin:$PATH"
ENV GOOGLE_GENAI_USE_VERTEXAI=1
ENV GOOGLE_CLOUD_LOCATION={gcp_region}
# Set up environment variables - End
# Install ADK - Start
RUN pip install google-adk=={adk_version}
# Install ADK - End
# Copy agent - Start
COPY "agents/{app_name}/" "/app/agents/{app_name}/"
{install_agent_deps}
# Copy agent - End
EXPOSE {port}
CMD adk {command} --port={port} {host_option} {session_db_option} {trace_to_cloud_option} "/app/agents"
"""
_AGENT_ENGINE_APP_TEMPLATE = """
from agent import root_agent
from vertexai.preview.reasoning_engines import AdkApp
adk_app = AdkApp(
  agent=root_agent,
  enable_tracing={trace_to_cloud_option},
)
"""
def _resolve_project(project_in_option: Optional[str]) -> str:
  if project_in_option:
    return project_in_option
  result = subprocess.run(
      ['gcloud', 'config', 'get-value', 'project'],
      check=True,
      capture_output=True,
      text=True,
  )
  project = result.stdout.strip()
  click.echo(f'Use default project: {project}')
  return project
def to_cloud_run(
    *,
    agent_folder: str,
    project: Optional[str],
    region: Optional[str],
    service_name: str,
    app_name: str,
    temp_folder: str,
    port: int,
    trace_to_cloud: bool,
    with_ui: bool,
    verbosity: str,
    session_db_url: str,
    artifact_storage_uri: Optional[str],
    adk_version: str,
):
  """Deploys an agent to Google Cloud Run.
  `agent_folder` should contain the following files:
  - __init__.py
  - agent.py
  - ... (other required source files)
  The folder structure of temp_folder will be
  * dist/[google_adk wheel file]
  * agents/[app_name]/
    * agent source code from `agent_folder`
  Args:
    agent_folder: The folder (absolute path) containing the agent source code.
    project: Google Cloud project id.
    region: Google Cloud region.
    service_name: The service name in Cloud Run.
    app_name: The name of the app, by default, it's basename of `agent_folder`.
    temp_folder: The temp folder for the generated Cloud Run source files.
    port: The port of the ADK api server.
    trace_to_cloud: Whether to enable Cloud Trace.
    with_ui: Whether to deploy with UI.
    verbosity: The verbosity level of the CLI.
    session_db_url: The database URL to connect the session.
    artifact_storage_uri: The artifact storage URI to store the artifacts.
    adk_version: The ADK version to use in Cloud Run.
  """
  app_name = app_name or os.path.basename(agent_folder)
  click.echo(f'Start generating Cloud Run source files in {temp_folder}')
  # remove temp_folder if exists
  if os.path.exists(temp_folder):
    click.echo('Removing existing files')
    shutil.rmtree(temp_folder)
  try:
    # copy agent source code
    click.echo('Copying agent source code...')
    agent_src_path = os.path.join(temp_folder, 'agents', app_name)
    shutil.copytree(agent_folder, agent_src_path)
    install_agent_deps = (
        else ''
    )
    click.echo('Copying agent source code complete.')
    host_option = '--host=0.0.0.0' if adk_version > '0.5.0' else ''
        gcp_project_id=project,
        gcp_region=region,
        app_name=app_name,
        port=port,
        command='web' if with_ui else 'api_server',
        install_agent_deps=install_agent_deps,
        session_db_option=f'--session_db_url={session_db_url}'
        if session_db_url
        else '',
        artifact_storage_option=f'--artifact_storage_uri={artifact_storage_uri}'
        if artifact_storage_uri
        else '',
        trace_to_cloud_option='--trace_to_cloud' if trace_to_cloud else '',
        adk_version=adk_version,
        host_option=host_option,
    )
    os.makedirs(temp_folder, exist_ok=True)
      f.write(
      )
    # Deploy to Cloud Run
    click.echo('Deploying to Cloud Run...')
    region_options = ['--region', region] if region else []
    project = _resolve_project(project)
    subprocess.run(
        [
            'gcloud',
            'run',
            'deploy',
            service_name,
            '--source',
            temp_folder,
            '--project',
            project,
            *region_options,
            '--port',
            str(port),
            '--verbosity',
            verbosity,
            '--labels',
            'created-by=adk',
        ],
        check=True,
    )
  finally:
    click.echo(f'Cleaning up the temp folder: {temp_folder}')
    shutil.rmtree(temp_folder)
def to_agent_engine(
    *,
    agent_folder: str,
    temp_folder: str,
    adk_app: str,
    project: str,
    region: str,
    staging_bucket: str,
    trace_to_cloud: bool,
    env_file: Optional[str] = None,
):
  """Deploys an agent to Vertex AI Agent Engine.
  `agent_folder` should contain the following files:
  - __init__.py
  - agent.py
  - <adk_app>.py (optional, for customization; will be autogenerated otherwise)
  - .env (optional, for environment variables)
  - ... (other required source files)
  The contents of `adk_app` should look something like:
  ```
  from agent import root_agent
  from vertexai.preview.reasoning_engines import AdkApp
  adk_app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
  )
  ```
  Args:
    agent_folder (str): The folder (absolute path) containing the agent source
      code.
    temp_folder (str): The temp folder for the generated Agent Engine source
      files. It will be replaced with the generated files if it already exists.
    project (str): Google Cloud project id.
    region (str): Google Cloud region.
    staging_bucket (str): The GCS bucket for staging the deployment artifacts.
    trace_to_cloud (bool): Whether to enable Cloud Trace.
      be used.
    env_file (str): The filepath to the `.env` file for environment variables.
      If not specified, the `.env` file in the `agent_folder` will be used.
  """
  # remove temp_folder if it exists
  if os.path.exists(temp_folder):
    click.echo('Removing existing files')
    shutil.rmtree(temp_folder)
  try:
    click.echo('Copying agent source code...')
    shutil.copytree(agent_folder, temp_folder)
    click.echo('Copying agent source code complete.')
    click.echo('Initializing Vertex AI...')
    import sys
    import vertexai
    from vertexai import agent_engines
    sys.path.append(temp_folder)
    vertexai.init(
        project=_resolve_project(project),
        location=region,
        staging_bucket=staging_bucket,
    )
    click.echo('Vertex AI initialized.')
    click.echo('Resolving files and dependencies...')
          f.write('google-cloud-aiplatform[adk,agent_engines]')
    env_vars = None
    if not env_file:
      # Attempt to read the env variables from .env in the dir (if any).
      env_file = os.path.join(temp_folder, '.env')
    if os.path.exists(env_file):
      from dotenv import dotenv_values
      click.echo(f'Reading environment variables from {env_file}')
      env_vars = dotenv_values(env_file)
    adk_app_file = f'{adk_app}.py'
    with open(
        os.path.join(temp_folder, adk_app_file), 'w', encoding='utf-8'
    ) as f:
      f.write(
          _AGENT_ENGINE_APP_TEMPLATE.format(
              trace_to_cloud_option=trace_to_cloud
          )
      )
    click.echo(f'Created {os.path.join(temp_folder, adk_app_file)}')
    click.echo('Files and dependencies resolved')
    click.echo('Deploying to agent engine...')
    agent_engine = agent_engines.ModuleAgent(
        module_name=adk_app,
        agent_name='adk_app',
        register_operations={
            '': [
                'get_session',
                'list_sessions',
                'create_session',
                'delete_session',
            ],
            'async': [
                'async_get_session',
                'async_list_sessions',
                'async_create_session',
                'async_delete_session',
            ],
            'async_stream': ['async_stream_query'],
            'stream': ['stream_query', 'streaming_agent_run_with_events'],
        },
        sys_paths=[temp_folder[1:]],
    )
    agent_engines.create(
        agent_engine=agent_engine,
        env_vars=env_vars,
        extra_packages=[temp_folder],
    )
  finally:
    click.echo(f'Cleaning up the temp folder: {temp_folder}')
    shutil.rmtree(temp_folder)
================================================
File: src/google/adk/cli/cli_eval.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import importlib.util
import json
import logging
import os
import sys
from typing import Any
from typing import AsyncGenerator
from typing import Optional
import uuid
from ..agents import Agent
from ..artifacts.base_artifact_service import BaseArtifactService
from ..evaluation.eval_case import EvalCase
from ..evaluation.eval_metrics import EvalMetric
from ..evaluation.eval_metrics import EvalMetricResult
from ..evaluation.eval_metrics import EvalMetricResultPerInvocation
from ..evaluation.eval_result import EvalCaseResult
from ..evaluation.evaluator import EvalStatus
from ..evaluation.evaluator import Evaluator
from ..sessions.base_session_service import BaseSessionService
logger = logging.getLogger("google_adk." + __name__)
    "Eval module is not installed, please install via `pip install"
    " google-adk[eval]`."
)
TOOL_TRAJECTORY_SCORE_KEY = "tool_trajectory_avg_score"
RESPONSE_MATCH_SCORE_KEY = "response_match_score"
# This evaluation is not very stable.
# This is always optional unless explicitly specified.
RESPONSE_EVALUATION_SCORE_KEY = "response_evaluation_score"
DEFAULT_CRITERIA = {
    TOOL_TRAJECTORY_SCORE_KEY: 1.0,  # 1-point scale; 1.0 is perfect.
    RESPONSE_MATCH_SCORE_KEY: 0.8,
}
def _import_from_path(module_name, file_path):
  spec = importlib.util.spec_from_file_location(module_name, file_path)
  module = importlib.util.module_from_spec(spec)
  sys.modules[module_name] = module
  spec.loader.exec_module(module)
  return module
def _get_agent_module(agent_module_file_path: str):
  file_path = os.path.join(agent_module_file_path, "__init__.py")
  module_name = "agent"
  return _import_from_path(module_name, file_path)
def get_evaluation_criteria_or_default(
    eval_config_file_path: str,
) -> dict[str, float]:
  """Returns evaluation criteria from the config file, if present.
  Otherwise a default one is returned.
  """
  if eval_config_file_path:
    with open(eval_config_file_path, "r", encoding="utf-8") as f:
      config_data = json.load(f)
    if "criteria" in config_data and isinstance(config_data["criteria"], dict):
      evaluation_criteria = config_data["criteria"]
    else:
      raise ValueError(
          " Expected a 'criteria' dictionary."
      )
  else:
    logger.info("No config file supplied. Using default criteria.")
    evaluation_criteria = DEFAULT_CRITERIA
  return evaluation_criteria
def get_root_agent(agent_module_file_path: str) -> Agent:
  """Returns root agent given the agent module."""
  agent_module = _get_agent_module(agent_module_file_path)
  root_agent = agent_module.agent.root_agent
  return root_agent
def try_get_reset_func(agent_module_file_path: str) -> Any:
  """Returns reset function for the agent, if present, given the agent module."""
  agent_module = _get_agent_module(agent_module_file_path)
  reset_func = getattr(agent_module.agent, "reset_data", None)
  return reset_func
def parse_and_get_evals_to_run(
    eval_set_file_path: tuple[str],
) -> dict[str, list[str]]:
  """Returns a dictionary of eval sets to evals that should be run."""
  eval_set_to_evals = {}
  for input_eval_set in eval_set_file_path:
    evals = []
    if ":" not in input_eval_set:
      eval_set_file = input_eval_set
    else:
      eval_set_file = input_eval_set.split(":")[0]
      evals = input_eval_set.split(":")[1].split(",")
    if eval_set_file not in eval_set_to_evals:
      eval_set_to_evals[eval_set_file] = []
    eval_set_to_evals[eval_set_file].extend(evals)
  return eval_set_to_evals
async def run_evals(
    eval_cases_by_eval_set_id: dict[str, list[EvalCase]],
    root_agent: Agent,
    reset_func: Optional[Any],
    eval_metrics: list[EvalMetric],
    session_service: Optional[BaseSessionService] = None,
    artifact_service: Optional[BaseArtifactService] = None,
) -> AsyncGenerator[EvalCaseResult, None]:
  """Returns a stream of EvalCaseResult for each eval case that was evaluated.
  Args:
    eval_cases_by_eval_set_id: Eval cases categorized by eval set id to which
      they belong.
    root_agent: Agent to use for inferencing.
    reset_func: If present, this will be called before invoking the agent before
      every inferencing step.
    eval_metrics: A list of metrics that should be used during evaluation.
    session_service: The session service to use during inferencing.
    artifact_service: The artifact service to use during inferencing.
  """
  try:
    from ..evaluation.agent_evaluator import EvaluationGenerator
  except ModuleNotFoundError as e:
  for eval_set_id, eval_cases in eval_cases_by_eval_set_id.items():
    for eval_case in eval_cases:
      eval_name = eval_case.eval_id
      initial_session = eval_case.session_input
      try:
        print(f"Running Eval: {eval_set_id}:{eval_name}")
        inference_result = (
            await EvaluationGenerator._generate_inferences_from_root_agent(
                invocations=eval_case.conversation,
                root_agent=root_agent,
                reset_func=reset_func,
                initial_session=initial_session,
                session_id=session_id,
                session_service=session_service,
                artifact_service=artifact_service,
            )
        )
        # Initialize the per-invocation metric results to an empty list.
        # We will fill this as we evaluate each metric.
        eval_metric_result_per_invocation = []
        for actual, expected in zip(inference_result, eval_case.conversation):
          eval_metric_result_per_invocation.append(
              EvalMetricResultPerInvocation(
                  actual_invocation=actual,
                  expected_invocation=expected,
                  eval_metric_results=[],
              )
          )
        overall_eval_metric_results = []
        for eval_metric in eval_metrics:
          metric_evaluator = _get_evaluator(eval_metric)
          evaluation_result = metric_evaluator.evaluate_invocations(
              actual_invocations=inference_result,
              expected_invocations=eval_case.conversation,
          )
          overall_eval_metric_results.append(
              EvalMetricResult(
                  metric_name=eval_metric.metric_name,
                  threshold=eval_metric.threshold,
                  score=evaluation_result.overall_score,
                  eval_status=evaluation_result.overall_eval_status,
              )
          )
          for index, per_invocation_result in enumerate(
              evaluation_result.per_invocation_results
          ):
            eval_metric_result_per_invocation[index].eval_metric_results.append(
                EvalMetricResult(
                    metric_name=eval_metric.metric_name,
                    threshold=eval_metric.threshold,
                    score=per_invocation_result.score,
                    eval_status=per_invocation_result.eval_status,
                )
            )
        final_eval_status = EvalStatus.NOT_EVALUATED
        # Go over the all the eval statuses and mark the final eval status as
        # passed if all of them pass, otherwise mark the final eval status to
        # failed.
        for overall_eval_metric_result in overall_eval_metric_results:
          overall_eval_status = overall_eval_metric_result.eval_status
          if overall_eval_status == EvalStatus.PASSED:
            final_eval_status = EvalStatus.PASSED
          elif overall_eval_status == EvalStatus.NOT_EVALUATED:
            continue
          elif overall_eval_status == EvalStatus.FAILED:
            final_eval_status = EvalStatus.FAILED
            break
          else:
            raise ValueError("Unknown eval status.")
        yield EvalCaseResult(
            eval_set_file=eval_set_id,
            eval_set_id=eval_set_id,
            eval_id=eval_name,
            final_eval_status=final_eval_status,
            eval_metric_results=[],
            overall_eval_metric_results=overall_eval_metric_results,
            eval_metric_result_per_invocation=eval_metric_result_per_invocation,
            session_id=session_id,
            user_id=user_id,
        )
        if final_eval_status == EvalStatus.PASSED:
          result = "✅ Passed"
        else:
          result = "❌ Failed"
        print(f"Result: {result}\n")
      except Exception:
        # Catching the general exception, so that we don't block other eval
        # cases.
        logger.exception(f"Eval failed for `{eval_set_id}:{eval_name}`")
def _get_evaluator(eval_metric: EvalMetric) -> Evaluator:
  try:
    from ..evaluation.response_evaluator import ResponseEvaluator
    from ..evaluation.trajectory_evaluator import TrajectoryEvaluator
  except ModuleNotFoundError as e:
  if eval_metric.metric_name == TOOL_TRAJECTORY_SCORE_KEY:
    return TrajectoryEvaluator(threshold=eval_metric.threshold)
  elif (
      eval_metric.metric_name == RESPONSE_MATCH_SCORE_KEY
      or eval_metric.metric_name == RESPONSE_EVALUATION_SCORE_KEY
  ):
    return ResponseEvaluator(
        threshold=eval_metric.threshold, metric_name=eval_metric.metric_name
    )
  raise ValueError(f"Unsupported eval metric: {eval_metric}")
================================================
File: src/google/adk/cli/cli_tools_click.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import asyncio
import collections
from contextlib import asynccontextmanager
from datetime import datetime
import functools
import logging
import os
import tempfile
from typing import Optional
import click
from fastapi import FastAPI
import uvicorn
from . import cli_create
from . import cli_deploy
from .. import version
from ..evaluation.local_eval_set_results_manager import LocalEvalSetResultsManager
from ..sessions.in_memory_session_service import InMemorySessionService
from .cli import run_cli
from .fast_api import get_fast_api_app
from .utils import envs
from .utils import logs
class HelpfulCommand(click.Command):
  """Command that shows full help on error instead of just the error message.
  A custom Click Command class that overrides the default error handling
  behavior to display the full help text when a required argument is missing,
  followed by the error message. This provides users with better context
  about command usage without needing to run a separate --help command.
  Args:
    *args: Variable length argument list to pass to the parent class.
    **kwargs: Arbitrary keyword arguments to pass to the parent class.
  Returns:
    None. Inherits behavior from the parent Click Command class.
  Returns:
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  @staticmethod
  def _format_missing_arg_error(click_exception):
    """Format the missing argument error with uppercase parameter name.
    Args:
      click_exception: The MissingParameter exception from Click.
    Returns:
      str: Formatted error message with uppercase parameter name.
    """
    name = click_exception.param.name
    return f"Missing required argument: {name.upper()}"
  def parse_args(self, ctx, args):
    """Override the parse_args method to show help text on error.
    Args:
      ctx: Click context object for the current command.
      args: List of command-line arguments to parse.
    Returns:
      The parsed arguments as returned by the parent class's parse_args method.
    Raises:
      click.MissingParameter: When a required parameter is missing, but this
        is caught and handled by displaying the help text before exiting.
    """
    try:
      return super().parse_args(ctx, args)
    except click.MissingParameter as exc:
      error_message = self._format_missing_arg_error(exc)
      click.echo(ctx.get_help())
      click.secho(f"\nError: {error_message}", fg="red", err=True)
      ctx.exit(2)
logger = logging.getLogger("google_adk." + __name__)
@click.group(context_settings={"max_content_width": 240})
@click.version_option(version.__version__)
def main():
  """Agent Development Kit CLI tools."""
  pass
@main.group()
def deploy():
  """Deploys agent to hosted environments."""
  pass
@main.command("create", cls=HelpfulCommand)
@click.option(
    "--model",
    type=str,
    help="Optional. The model used for the root agent.",
)
@click.option(
    "--api_key",
    type=str,
    help=(
        "Optional. The API Key needed to access the model, e.g. Google AI API"
        " Key."
    ),
)
@click.option(
    "--project",
    type=str,
    help="Optional. The Google Cloud Project for using VertexAI as backend.",
)
@click.option(
    "--region",
    type=str,
    help="Optional. The Google Cloud Region for using VertexAI as backend.",
)
@click.argument("app_name", type=str, required=True)
def cli_create_cmd(
    app_name: str,
    model: Optional[str],
    api_key: Optional[str],
    project: Optional[str],
    region: Optional[str],
):
  """Creates a new app in the current folder with prepopulated agent template.
  APP_NAME: required, the folder of the agent source code.
  Example:
    adk create path/to/my_app
  """
  cli_create.run_cmd(
      app_name,
      model=model,
      google_api_key=api_key,
      google_cloud_project=project,
      google_cloud_region=region,
  )
def validate_exclusive(ctx, param, value):
  # Store the validated parameters in the context
  if not hasattr(ctx, "exclusive_opts"):
    ctx.exclusive_opts = {}
  # If this option has a value and we've already seen another exclusive option
  if value is not None and any(ctx.exclusive_opts.values()):
    exclusive_opt = next(key for key, val in ctx.exclusive_opts.items() if val)
    raise click.UsageError(
        f"Options '{param.name}' and '{exclusive_opt}' cannot be set together."
    )
  # Record this option's value
  ctx.exclusive_opts[param.name] = value is not None
  return value
@main.command("run", cls=HelpfulCommand)
@click.option(
    "--save_session",
    type=bool,
    is_flag=True,
    show_default=True,
    default=False,
    help="Optional. Whether to save the session to a json file on exit.",
)
@click.option(
    "--session_id",
    type=str,
    help=(
        "Optional. The session ID to save the session to on exit when"
        " --save_session is set to true. User will be prompted to enter a"
        " session ID if not set."
    ),
)
@click.option(
    "--replay",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, resolve_path=True
    ),
    help=(
        "The json file that contains the initial state of the session and user"
        " queries. A new session will be created using this state. And user"
        " queries are run againt the newly created session. Users cannot"
        " continue to interact with the agent."
    ),
    callback=validate_exclusive,
)
@click.option(
    "--resume",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, resolve_path=True
    ),
    help=(
        "The json file that contains a previously saved session (by"
        "--save_session option). The previous session will be re-displayed. And"
        " user can continue to interact with the agent."
    ),
    callback=validate_exclusive,
)
@click.argument(
    "agent",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, resolve_path=True
    ),
)
def cli_run(
    agent: str,
    save_session: bool,
    session_id: Optional[str],
    replay: Optional[str],
    resume: Optional[str],
):
  """Runs an interactive CLI for a certain agent.
  AGENT: The path to the agent source code folder.
  Example:
    adk run path/to/my_agent
  """
  logs.log_to_tmp_folder()
  agent_parent_folder = os.path.dirname(agent)
  agent_folder_name = os.path.basename(agent)
  asyncio.run(
      run_cli(
          agent_parent_dir=agent_parent_folder,
          agent_folder_name=agent_folder_name,
          input_file=replay,
          saved_session_file=resume,
          save_session=save_session,
          session_id=session_id,
      )
  )
@main.command("eval", cls=HelpfulCommand)
@click.argument(
    "agent_module_file_path",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, resolve_path=True
    ),
)
@click.argument("eval_set_file_path", nargs=-1)
@click.option("--config_file_path", help="Optional. The path to config file.")
@click.option(
    "--print_detailed_results",
    is_flag=True,
    show_default=True,
    default=False,
    help="Optional. Whether to print detailed results on console or not.",
)
def cli_eval(
    agent_module_file_path: str,
    eval_set_file_path: tuple[str],
    config_file_path: str,
    print_detailed_results: bool,
):
  """Evaluates an agent given the eval sets.
  AGENT_MODULE_FILE_PATH: The path to the __init__.py file that contains a
  module by the name "agent". "agent" module contains a root_agent.
  EVAL_SET_FILE_PATH: You can specify one or more eval set file paths.
  For each file, all evals will be run by default.
  If you want to run only specific evals from a eval set, first create a comma
  separated list of eval names and then add that as a suffix to the eval set
  file name, demarcated by a `:`.
  For example,
  sample_eval_set_file.json:eval_1,eval_2,eval_3
  This will only run eval_1, eval_2 and eval_3 from sample_eval_set_file.json.
  CONFIG_FILE_PATH: The path to config file.
  """
  envs.load_dotenv_for_agent(agent_module_file_path, ".")
  try:
    from ..evaluation.local_eval_sets_manager import load_eval_set_from_file
    from .cli_eval import EvalCaseResult
    from .cli_eval import EvalMetric
    from .cli_eval import EvalStatus
    from .cli_eval import get_evaluation_criteria_or_default
    from .cli_eval import get_root_agent
    from .cli_eval import parse_and_get_evals_to_run
    from .cli_eval import run_evals
    from .cli_eval import try_get_reset_func
  except ModuleNotFoundError:
  evaluation_criteria = get_evaluation_criteria_or_default(config_file_path)
  eval_metrics = []
  for metric_name, threshold in evaluation_criteria.items():
    eval_metrics.append(
        EvalMetric(metric_name=metric_name, threshold=threshold)
    )
  print(f"Using evaluation criteria: {evaluation_criteria}")
  root_agent = get_root_agent(agent_module_file_path)
  reset_func = try_get_reset_func(agent_module_file_path)
  eval_set_file_path_to_evals = parse_and_get_evals_to_run(eval_set_file_path)
  eval_set_id_to_eval_cases = {}
  # Read the eval_set files and get the cases.
  for eval_set_file_path, eval_case_ids in eval_set_file_path_to_evals.items():
    eval_set = load_eval_set_from_file(eval_set_file_path, eval_set_file_path)
    eval_cases = eval_set.eval_cases
    if eval_case_ids:
      # There are eval_ids that we should select.
      eval_cases = [
          e for e in eval_set.eval_cases if e.eval_id in eval_case_ids
      ]
    eval_set_id_to_eval_cases[eval_set.eval_set_id] = eval_cases
  async def _collect_eval_results() -> list[EvalCaseResult]:
    session_service = InMemorySessionService()
    eval_case_results = []
    async for eval_case_result in run_evals(
        eval_set_id_to_eval_cases,
        root_agent,
        reset_func,
        eval_metrics,
        session_service=session_service,
    ):
      eval_case_result.session_details = await session_service.get_session(
          app_name=os.path.basename(agent_module_file_path),
          user_id=eval_case_result.user_id,
          session_id=eval_case_result.session_id,
      )
      eval_case_results.append(eval_case_result)
    return eval_case_results
  try:
    eval_results = asyncio.run(_collect_eval_results())
  except ModuleNotFoundError:
  # Write eval set results.
  local_eval_set_results_manager = LocalEvalSetResultsManager(
      agents_dir=os.path.dirname(agent_module_file_path)
  )
  eval_set_id_to_eval_results = collections.defaultdict(list)
  for eval_case_result in eval_results:
    eval_set_id = eval_case_result.eval_set_id
    eval_set_id_to_eval_results[eval_set_id].append(eval_case_result)
  for eval_set_id, eval_case_results in eval_set_id_to_eval_results.items():
    local_eval_set_results_manager.save_eval_set_result(
        app_name=os.path.basename(agent_module_file_path),
        eval_set_id=eval_set_id,
        eval_case_results=eval_case_results,
    )
  print("*********************************************************************")
  eval_run_summary = {}
  for eval_result in eval_results:
    eval_result: EvalCaseResult
    if eval_result.eval_set_id not in eval_run_summary:
      eval_run_summary[eval_result.eval_set_id] = [0, 0]
    if eval_result.final_eval_status == EvalStatus.PASSED:
      eval_run_summary[eval_result.eval_set_id][0] += 1
    else:
      eval_run_summary[eval_result.eval_set_id][1] += 1
  print("Eval Run Summary")
  for eval_set_id, pass_fail_count in eval_run_summary.items():
    print(
        f" failed: {pass_fail_count[1]}"
    )
  if print_detailed_results:
    for eval_result in eval_results:
      eval_result: EvalCaseResult
      print(
          "*********************************************************************"
      )
      print(eval_result.model_dump_json(indent=2))
def fast_api_common_options():
  """Decorator to add common fast api options to click commands."""
  def decorator(func):
    @click.option(
        "--session_db_url",
        help=(
            """Optional. The database URL to store the session.
          - Use 'agentengine://<agent_engine_resource_id>' to connect to Agent Engine sessions.
          - Use 'sqlite://<path_to_sqlite_file>' to connect to a SQLite DB.
          - See https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls for more details on supported DB URLs."""
        ),
    )
    @click.option(
        "--artifact_storage_uri",
        type=str,
        help=(
            "Optional. The artifact storage URI to store the artifacts,"
            " supported URIs: gs://<bucket name> for GCS artifact service."
        ),
        default=None,
    )
    @click.option(
        "--host",
        type=str,
        help="Optional. The binding host of the server",
        default="127.0.0.1",
        show_default=True,
    )
    @click.option(
        "--port",
        type=int,
        help="Optional. The port of the server",
        default=8000,
    )
    @click.option(
        "--allow_origins",
        help="Optional. Any additional origins to allow for CORS.",
        multiple=True,
    )
    @click.option(
        "--log_level",
        type=click.Choice(
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            case_sensitive=False,
        ),
        default="INFO",
        help="Optional. Set the logging level",
    )
    @click.option(
        "--trace_to_cloud",
        is_flag=True,
        show_default=True,
        default=False,
        help="Optional. Whether to enable cloud trace for telemetry.",
    )
    @click.option(
        "--reload/--no-reload",
        default=True,
        help="Optional. Whether to enable auto reload for server.",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      return func(*args, **kwargs)
    return wrapper
  return decorator
@main.command("web")
@fast_api_common_options()
@click.argument(
    "agents_dir",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, resolve_path=True
    ),
    default=os.getcwd,
)
def cli_web(
    agents_dir: str,
    session_db_url: str = "",
    artifact_storage_uri: Optional[str] = None,
    log_level: str = "INFO",
    allow_origins: Optional[list[str]] = None,
    host: str = "127.0.0.1",
    port: int = 8000,
    trace_to_cloud: bool = False,
    reload: bool = True,
):
  """Starts a FastAPI server with Web UI for agents.
  AGENTS_DIR: The directory of agents, where each sub-directory is a single
  agent, containing at least `__init__.py` and `agent.py` files.
  Example:
    adk web --session_db_url=[db_url] --port=[port] path/to/agents_dir
  """
  logs.setup_adk_logger(getattr(logging, log_level.upper()))
  @asynccontextmanager
  async def _lifespan(app: FastAPI):
    click.secho(
        f"""
+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
+-----------------------------------------------------------------------------+
""",
        fg="green",
    )
    yield  # Startup is done, now app is running
    click.secho(
        """
+-----------------------------------------------------------------------------+
| ADK Web Server shutting down...                                             |
+-----------------------------------------------------------------------------+
""",
        fg="green",
    )
  app = get_fast_api_app(
      agents_dir=agents_dir,
      session_db_url=session_db_url,
      artifact_storage_uri=artifact_storage_uri,
      allow_origins=allow_origins,
      web=True,
      trace_to_cloud=trace_to_cloud,
      lifespan=_lifespan,
  )
  config = uvicorn.Config(
      app,
      host=host,
      port=port,
      reload=reload,
  )
  server = uvicorn.Server(config)
  server.run()
@main.command("api_server")
# The directory of agents, where each sub-directory is a single agent.
# By default, it is the current working directory
@click.argument(
    "agents_dir",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, resolve_path=True
    ),
    default=os.getcwd(),
)
@fast_api_common_options()
def cli_api_server(
    agents_dir: str,
    session_db_url: str = "",
    artifact_storage_uri: Optional[str] = None,
    log_level: str = "INFO",
    allow_origins: Optional[list[str]] = None,
    host: str = "127.0.0.1",
    port: int = 8000,
    trace_to_cloud: bool = False,
    reload: bool = True,
):
  """Starts a FastAPI server for agents.
  AGENTS_DIR: The directory of agents, where each sub-directory is a single
  agent, containing at least `__init__.py` and `agent.py` files.
  Example:
    adk api_server --session_db_url=[db_url] --port=[port] path/to/agents_dir
  """
  logs.setup_adk_logger(getattr(logging, log_level.upper()))
  config = uvicorn.Config(
      get_fast_api_app(
          agents_dir=agents_dir,
          session_db_url=session_db_url,
          artifact_storage_uri=artifact_storage_uri,
          allow_origins=allow_origins,
          web=False,
          trace_to_cloud=trace_to_cloud,
      ),
      host=host,
      port=port,
      reload=reload,
  )
  server = uvicorn.Server(config)
  server.run()
@deploy.command("cloud_run")
@click.option(
    "--project",
    type=str,
    help=(
        "Required. Google Cloud project to deploy the agent. When absent,"
        " default project from gcloud config is used."
    ),
)
@click.option(
    "--region",
    type=str,
    help=(
        "Required. Google Cloud region to deploy the agent. When absent,"
        " gcloud run deploy will prompt later."
    ),
)
@click.option(
    "--service_name",
    type=str,
    default="adk-default-service-name",
    help=(
        "Optional. The service name to use in Cloud Run (default:"
        " 'adk-default-service-name')."
    ),
)
@click.option(
    "--app_name",
    type=str,
    default="",
    help=(
        "Optional. App name of the ADK API server (default: the folder name"
        " of the AGENT source code)."
    ),
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Optional. The port of the ADK API server (default: 8000).",
)
@click.option(
    "--trace_to_cloud",
    is_flag=True,
    show_default=True,
    default=False,
    help="Optional. Whether to enable Cloud Trace for cloud run.",
)
@click.option(
    "--with_ui",
    is_flag=True,
    show_default=True,
    default=False,
    help=(
        "Optional. Deploy ADK Web UI if set. (default: deploy ADK API server"
        " only)"
    ),
)
@click.option(
    "--temp_folder",
    type=str,
    default=os.path.join(
        tempfile.gettempdir(),
        "cloud_run_deploy_src",
        datetime.now().strftime("%Y%m%d_%H%M%S"),
    ),
    help=(
        "Optional. Temp folder for the generated Cloud Run source files"
        " (default: a timestamped folder in the system temp directory)."
    ),
)
@click.option(
    "--verbosity",
    type=click.Choice(
        ["debug", "info", "warning", "error", "critical"], case_sensitive=False
    ),
    default="WARNING",
    help="Optional. Override the default verbosity level.",
)
@click.option(
    "--session_db_url",
    help=(
        """Optional. The database URL to store the session.
  - Use 'agentengine://<agent_engine_resource_id>' to connect to Agent Engine sessions.
  - Use 'sqlite://<path_to_sqlite_file>' to connect to a SQLite DB.
  - See https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls for more details on supported DB URLs."""
    ),
)
@click.option(
    "--artifact_storage_uri",
    type=str,
    help=(
        "Optional. The artifact storage URI to store the artifacts, supported"
        " URIs: gs://<bucket name> for GCS artifact service."
    ),
    default=None,
)
@click.argument(
    "agent",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, resolve_path=True
    ),
)
@click.option(
    "--adk_version",
    type=str,
    default=version.__version__,
    show_default=True,
    help=(
        "Optional. The ADK version used in Cloud Run deployment. (default: the"
        " version in the dev environment)"
    ),
)
def cli_deploy_cloud_run(
    agent: str,
    project: Optional[str],
    region: Optional[str],
    service_name: str,
    app_name: str,
    temp_folder: str,
    port: int,
    trace_to_cloud: bool,
    with_ui: bool,
    verbosity: str,
    session_db_url: str,
    artifact_storage_uri: Optional[str],
    adk_version: str,
):
  """Deploys an agent to Cloud Run.
  AGENT: The path to the agent source code folder.
  Example:
    adk deploy cloud_run --project=[project] --region=[region] path/to/my_agent
  """
  try:
    cli_deploy.to_cloud_run(
        agent_folder=agent,
        project=project,
        region=region,
        service_name=service_name,
        app_name=app_name,
        temp_folder=temp_folder,
        port=port,
        trace_to_cloud=trace_to_cloud,
        with_ui=with_ui,
        verbosity=verbosity,
        session_db_url=session_db_url,
        artifact_storage_uri=artifact_storage_uri,
        adk_version=adk_version,
    )
  except Exception as e:
    click.secho(f"Deploy failed: {e}", fg="red", err=True)
@deploy.command("agent_engine")
@click.option(
    "--project",
    type=str,
    help="Required. Google Cloud project to deploy the agent.",
)
@click.option(
    "--region",
    type=str,
    help="Required. Google Cloud region to deploy the agent.",
)
@click.option(
    "--staging_bucket",
    type=str,
    help="Required. GCS bucket for staging the deployment artifacts.",
)
@click.option(
    "--trace_to_cloud",
    type=bool,
    is_flag=True,
    show_default=True,
    default=False,
    help="Optional. Whether to enable Cloud Trace for Agent Engine.",
)
@click.option(
    "--adk_app",
    type=str,
    default="agent_engine_app",
    help=(
        "Optional. Python file for defining the ADK application"
        " (default: a file named agent_engine_app.py)"
    ),
)
@click.option(
    "--temp_folder",
    type=str,
    default=os.path.join(
        tempfile.gettempdir(),
        "agent_engine_deploy_src",
        datetime.now().strftime("%Y%m%d_%H%M%S"),
    ),
    help=(
        "Optional. Temp folder for the generated Agent Engine source files."
        " If the folder already exists, its contents will be removed."
        " (default: a timestamped folder in the system temp directory)."
    ),
)
@click.option(
    "--env_file",
    type=str,
    default="",
    help=(
        "Optional. The filepath to the `.env` file for environment variables."
        " (default: the `.env` file in the `agent` directory, if any.)"
    ),
)
@click.option(
    type=str,
    default="",
    help=(
        " any.)"
    ),
)
@click.argument(
    "agent",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, resolve_path=True
    ),
)
def cli_deploy_agent_engine(
    agent: str,
    project: str,
    region: str,
    staging_bucket: str,
    trace_to_cloud: bool,
    adk_app: str,
    temp_folder: str,
    env_file: str,
):
  """Deploys an agent to Agent Engine.
  Args:
    agent (str): Required. The path to the agent to be deloyed.
    project (str): Required. Google Cloud project to deploy the agent.
    region (str): Required. Google Cloud region to deploy the agent.
    staging_bucket (str): Required. GCS bucket for staging the deployment
      artifacts.
    trace_to_cloud (bool): Required. Whether to enable Cloud Trace.
    adk_app (str): Required. Python file for defining the ADK application.
    temp_folder (str): Required. The folder for the generated Agent Engine
      files. If the folder already exists, its contents will be replaced.
    env_file (str): Required. The filepath to the `.env` file for environment
      variables. If it is an empty string, the `.env` file in the `agent`
      directory will be used if it exists.
      `agent` directory will be used if exists.
  Example:
    adk deploy agent_engine --project=[project] --region=[region]
      --staging_bucket=[staging_bucket] path/to/my_agent
  """
  try:
    cli_deploy.to_agent_engine(
        agent_folder=agent,
        project=project,
        region=region,
        staging_bucket=staging_bucket,
        trace_to_cloud=trace_to_cloud,
        adk_app=adk_app,
        temp_folder=temp_folder,
        env_file=env_file,
    )
  except Exception as e:
    click.secho(f"Deploy failed: {e}", fg="red", err=True)
================================================
File: src/google/adk/cli/fast_api.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path
import time
import traceback
import typing
from typing import Any
from typing import List
from typing import Literal
from typing import Optional
import click
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect
from google.genai import types
import graphviz
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import export
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace import TracerProvider
from pydantic import Field
from pydantic import ValidationError
from starlette.types import Lifespan
from typing_extensions import override
from ..agents import RunConfig
from ..agents.live_request_queue import LiveRequest
from ..agents.live_request_queue import LiveRequestQueue
from ..agents.llm_agent import Agent
from ..agents.run_config import StreamingMode
from ..artifacts.gcs_artifact_service import GcsArtifactService
from ..artifacts.in_memory_artifact_service import InMemoryArtifactService
from ..evaluation.eval_case import EvalCase
from ..evaluation.eval_case import SessionInput
from ..evaluation.eval_metrics import EvalMetric
from ..evaluation.eval_metrics import EvalMetricResult
from ..evaluation.eval_metrics import EvalMetricResultPerInvocation
from ..evaluation.eval_result import EvalSetResult
from ..evaluation.local_eval_set_results_manager import LocalEvalSetResultsManager
from ..evaluation.local_eval_sets_manager import LocalEvalSetsManager
from ..events.event import Event
from ..memory.in_memory_memory_service import InMemoryMemoryService
from ..runners import Runner
from ..sessions.database_session_service import DatabaseSessionService
from ..sessions.in_memory_session_service import InMemorySessionService
from ..sessions.session import Session
from ..sessions.vertex_ai_session_service import VertexAiSessionService
from .cli_eval import EvalStatus
from .utils import cleanup
from .utils import common
from .utils import create_empty_state
from .utils import envs
from .utils import evals
from .utils.agent_loader import AgentLoader
logger = logging.getLogger("google_adk." + __name__)
_EVAL_SET_FILE_EXTENSION = ".evalset.json"
class ApiServerSpanExporter(export.SpanExporter):
  def __init__(self, trace_dict):
    self.trace_dict = trace_dict
  def export(
      self, spans: typing.Sequence[ReadableSpan]
  ) -> export.SpanExportResult:
    for span in spans:
      if (
          span.name == "call_llm"
          or span.name == "send_data"
          or span.name.startswith("execute_tool")
      ):
        attributes = dict(span.attributes)
        attributes["trace_id"] = span.get_span_context().trace_id
        attributes["span_id"] = span.get_span_context().span_id
        if attributes.get("gcp.vertex.agent.event_id", None):
          self.trace_dict[attributes["gcp.vertex.agent.event_id"]] = attributes
    return export.SpanExportResult.SUCCESS
  def force_flush(self, timeout_millis: int = 30000) -> bool:
    return True
class InMemoryExporter(export.SpanExporter):
  def __init__(self, trace_dict):
    super().__init__()
    self._spans = []
    self.trace_dict = trace_dict
  @override
  def export(
      self, spans: typing.Sequence[ReadableSpan]
  ) -> export.SpanExportResult:
    for span in spans:
      trace_id = span.context.trace_id
      if span.name == "call_llm":
        attributes = dict(span.attributes)
        session_id = attributes.get("gcp.vertex.agent.session_id", None)
        if session_id:
          if session_id not in self.trace_dict:
            self.trace_dict[session_id] = [trace_id]
          else:
            self.trace_dict[session_id] += [trace_id]
    self._spans.extend(spans)
    return export.SpanExportResult.SUCCESS
  @override
  def force_flush(self, timeout_millis: int = 30000) -> bool:
    return True
  def get_finished_spans(self, session_id: str):
    trace_ids = self.trace_dict.get(session_id, None)
    if trace_ids is None or not trace_ids:
      return []
    return [x for x in self._spans if x.context.trace_id in trace_ids]
  def clear(self):
    self._spans.clear()
class AgentRunRequest(common.BaseModel):
  app_name: str
  user_id: str
  session_id: str
  new_message: types.Content
  streaming: bool = False
class AddSessionToEvalSetRequest(common.BaseModel):
  eval_id: str
  session_id: str
  user_id: str
class RunEvalRequest(common.BaseModel):
  eval_ids: list[str]  # if empty, then all evals in the eval set are run.
  eval_metrics: list[EvalMetric]
class RunEvalResult(common.BaseModel):
  eval_set_file: str
  eval_set_id: str
  eval_id: str
  final_eval_status: EvalStatus
  eval_metric_results: list[tuple[EvalMetric, EvalMetricResult]] = Field(
      deprecated=True,
      description=(
          "This field is deprecated, use overall_eval_metric_results instead."
      ),
  )
  overall_eval_metric_results: list[EvalMetricResult]
  eval_metric_result_per_invocation: list[EvalMetricResultPerInvocation]
  user_id: str
  session_id: str
class GetEventGraphResult(common.BaseModel):
  dot_src: str
def get_fast_api_app(
    *,
    agents_dir: str,
    session_db_url: str = "",
    artifact_storage_uri: Optional[str] = None,
    allow_origins: Optional[list[str]] = None,
    web: bool,
    trace_to_cloud: bool = False,
    lifespan: Optional[Lifespan[FastAPI]] = None,
) -> FastAPI:
  # InMemory tracing dict.
  trace_dict: dict[str, Any] = {}
  session_trace_dict: dict[str, Any] = {}
  # Set up tracing in the FastAPI server.
  provider = TracerProvider()
  provider.add_span_processor(
      export.SimpleSpanProcessor(ApiServerSpanExporter(trace_dict))
  )
  memory_exporter = InMemoryExporter(session_trace_dict)
  provider.add_span_processor(export.SimpleSpanProcessor(memory_exporter))
  if trace_to_cloud:
    envs.load_dotenv_for_agent("", agents_dir)
      processor = export.BatchSpanProcessor(
          CloudTraceSpanExporter(project_id=project_id)
      )
      provider.add_span_processor(processor)
    else:
      logger.warning(
          " not be enabled."
      )
  trace.set_tracer_provider(provider)
  @asynccontextmanager
  async def internal_lifespan(app: FastAPI):
    try:
      if lifespan:
        async with lifespan(app) as lifespan_context:
          yield lifespan_context
      else:
        yield
    finally:
      # Create tasks for all runner closures to run concurrently
      await cleanup.close_runners(list(runner_dict.values()))
  # Run the FastAPI server.
  app = FastAPI(lifespan=internal_lifespan)
  if allow_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
  runner_dict = {}
  eval_sets_manager = LocalEvalSetsManager(agents_dir=agents_dir)
  eval_set_results_manager = LocalEvalSetResultsManager(agents_dir=agents_dir)
  # Build the Memory service
  memory_service = InMemoryMemoryService()
  # Build the Session service
  agent_engine_id = ""
  if session_db_url:
    if session_db_url.startswith("agentengine://"):
      # Create vertex session service
      agent_engine_id = session_db_url.split("://")[1]
      if not agent_engine_id:
        raise click.ClickException("Agent engine id can not be empty.")
      envs.load_dotenv_for_agent("", agents_dir)
      session_service = VertexAiSessionService(
          os.environ["GOOGLE_CLOUD_LOCATION"],
      )
    else:
      session_service = DatabaseSessionService(db_url=session_db_url)
  else:
    session_service = InMemorySessionService()
  # Build the Artifact service
  if artifact_storage_uri:
    if artifact_storage_uri.startswith("gs://"):
      gcs_bucket = artifact_storage_uri.split("://")[1]
      artifact_service = GcsArtifactService(bucket_name=gcs_bucket)
    else:
      raise click.ClickException(
          "Unsupported artifact storage URI: %s" % artifact_storage_uri
      )
  else:
    artifact_service = InMemoryArtifactService()
  # initialize Agent Loader
  agent_loader = AgentLoader(agents_dir)
  @app.get("/list-apps")
  def list_apps() -> list[str]:
    base_path = Path.cwd() / agents_dir
    if not base_path.exists():
      raise HTTPException(status_code=404, detail="Path not found")
    if not base_path.is_dir():
      raise HTTPException(status_code=400, detail="Not a directory")
    agent_names = [
        x
        for x in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, x))
        and not x.startswith(".")
        and x != "__pycache__"
    ]
    agent_names.sort()
    return agent_names
  @app.get("/debug/trace/{event_id}")
  def get_trace_dict(event_id: str) -> Any:
    event_dict = trace_dict.get(event_id, None)
    if event_dict is None:
      raise HTTPException(status_code=404, detail="Trace not found")
    return event_dict
  @app.get("/debug/trace/session/{session_id}")
  def get_session_trace(session_id: str) -> Any:
    spans = memory_exporter.get_finished_spans(session_id)
    if not spans:
      return []
    return [
        {
            "name": s.name,
            "span_id": s.context.span_id,
            "trace_id": s.context.trace_id,
            "start_time": s.start_time,
            "end_time": s.end_time,
            "attributes": dict(s.attributes),
            "parent_span_id": s.parent.span_id if s.parent else None,
        }
        for s in spans
    ]
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
      response_model_exclude_none=True,
  )
  async def get_session(
      app_name: str, user_id: str, session_id: str
  ) -> Session:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    session = await session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    if not session:
      raise HTTPException(status_code=404, detail="Session not found")
    return session
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions",
      response_model_exclude_none=True,
  )
  async def list_sessions(app_name: str, user_id: str) -> list[Session]:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    list_sessions_response = await session_service.list_sessions(
        app_name=app_name, user_id=user_id
    )
    return [
        session
        for session in list_sessions_response.sessions
        # Remove sessions that were generated as a part of Eval.
    ]
  @app.post(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
      response_model_exclude_none=True,
  )
  async def create_session_with_id(
      app_name: str,
      user_id: str,
      session_id: str,
      state: Optional[dict[str, Any]] = None,
  ) -> Session:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    if (
        await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        is not None
    ):
      logger.warning("Session already exists: %s", session_id)
      raise HTTPException(
          status_code=400, detail=f"Session already exists: {session_id}"
      )
    logger.info("New session created: %s", session_id)
    return await session_service.create_session(
        app_name=app_name, user_id=user_id, state=state, session_id=session_id
    )
  @app.post(
      "/apps/{app_name}/users/{user_id}/sessions",
      response_model_exclude_none=True,
  )
  async def create_session(
      app_name: str,
      user_id: str,
      state: Optional[dict[str, Any]] = None,
  ) -> Session:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    logger.info("New session created")
    return await session_service.create_session(
        app_name=app_name, user_id=user_id, state=state
    )
  def _get_eval_set_file_path(app_name, agents_dir, eval_set_id) -> str:
    return os.path.join(
        agents_dir,
        app_name,
        eval_set_id + _EVAL_SET_FILE_EXTENSION,
    )
  @app.post(
      "/apps/{app_name}/eval_sets/{eval_set_id}",
      response_model_exclude_none=True,
  )
  def create_eval_set(
      app_name: str,
      eval_set_id: str,
  ):
    """Creates an eval set, given the id."""
    try:
      eval_sets_manager.create_eval_set(app_name, eval_set_id)
    except ValueError as ve:
      raise HTTPException(
          status_code=400,
          detail=str(ve),
      ) from ve
  @app.get(
      "/apps/{app_name}/eval_sets",
      response_model_exclude_none=True,
  )
  def list_eval_sets(app_name: str) -> list[str]:
    """Lists all eval sets for the given app."""
    return eval_sets_manager.list_eval_sets(app_name)
  @app.post(
      "/apps/{app_name}/eval_sets/{eval_set_id}/add_session",
      response_model_exclude_none=True,
  )
  async def add_session_to_eval_set(
      app_name: str, eval_set_id: str, req: AddSessionToEvalSetRequest
  ):
    # Get the session
    session = await session_service.get_session(
        app_name=app_name, user_id=req.user_id, session_id=req.session_id
    )
    assert session, "Session not found."
    # Convert the session data to eval invocations
    invocations = evals.convert_session_to_eval_invocations(session)
    # Populate the session with initial session state.
    initial_session_state = create_empty_state(
        agent_loader.load_agent(app_name)
    )
    new_eval_case = EvalCase(
        eval_id=req.eval_id,
        conversation=invocations,
        session_input=SessionInput(
            app_name=app_name, user_id=req.user_id, state=initial_session_state
        ),
        creation_timestamp=time.time(),
    )
    try:
      eval_sets_manager.add_eval_case(app_name, eval_set_id, new_eval_case)
    except ValueError as ve:
      raise HTTPException(status_code=400, detail=str(ve)) from ve
  @app.get(
      "/apps/{app_name}/eval_sets/{eval_set_id}/evals",
      response_model_exclude_none=True,
  )
  def list_evals_in_eval_set(
      app_name: str,
      eval_set_id: str,
  ) -> list[str]:
    """Lists all evals in an eval set."""
    eval_set_data = eval_sets_manager.get_eval_set(app_name, eval_set_id)
    return sorted([x.eval_id for x in eval_set_data.eval_cases])
  @app.post(
      "/apps/{app_name}/eval_sets/{eval_set_id}/run_eval",
      response_model_exclude_none=True,
  )
  async def run_eval(
      app_name: str, eval_set_id: str, req: RunEvalRequest
  ) -> list[RunEvalResult]:
    """Runs an eval given the details in the eval request."""
    from .cli_eval import run_evals
    # Create a mapping from eval set file to all the evals that needed to be
    # run.
    eval_set = eval_sets_manager.get_eval_set(app_name, eval_set_id)
    if req.eval_ids:
      eval_cases = [e for e in eval_set.eval_cases if e.eval_id in req.eval_ids]
      eval_set_to_evals = {eval_set_id: eval_cases}
    else:
      logger.info("Eval ids to run list is empty. We will run all eval cases.")
      eval_set_to_evals = {eval_set_id: eval_set.eval_cases}
    root_agent = agent_loader.load_agent(app_name)
    run_eval_results = []
    eval_case_results = []
    try:
      async for eval_case_result in run_evals(
          eval_set_to_evals,
          root_agent,
          getattr(root_agent, "reset_data", None),
          req.eval_metrics,
          session_service=session_service,
          artifact_service=artifact_service,
      ):
        run_eval_results.append(
            RunEvalResult(
                app_name=app_name,
                eval_set_file=eval_case_result.eval_set_file,
                eval_set_id=eval_set_id,
                eval_id=eval_case_result.eval_id,
                final_eval_status=eval_case_result.final_eval_status,
                eval_metric_results=eval_case_result.eval_metric_results,
                overall_eval_metric_results=eval_case_result.overall_eval_metric_results,
                eval_metric_result_per_invocation=eval_case_result.eval_metric_result_per_invocation,
                user_id=eval_case_result.user_id,
                session_id=eval_case_result.session_id,
            )
        )
        eval_case_result.session_details = await session_service.get_session(
            app_name=app_name,
            user_id=eval_case_result.user_id,
            session_id=eval_case_result.session_id,
        )
        eval_case_results.append(eval_case_result)
    except ModuleNotFoundError as e:
      logger.exception("%s", e)
      raise HTTPException(status_code=400, detail=str(e)) from e
    eval_set_results_manager.save_eval_set_result(
        app_name, eval_set_id, eval_case_results
    )
    return run_eval_results
  @app.get(
      "/apps/{app_name}/eval_results/{eval_result_id}",
      response_model_exclude_none=True,
  )
  def get_eval_result(
      app_name: str,
      eval_result_id: str,
  ) -> EvalSetResult:
    """Gets the eval result for the given eval id."""
    try:
      return eval_set_results_manager.get_eval_set_result(
          app_name, eval_result_id
      )
    except ValueError as ve:
      raise HTTPException(status_code=404, detail=str(ve)) from ve
    except ValidationError as ve:
      raise HTTPException(status_code=500, detail=str(ve)) from ve
  @app.get(
      "/apps/{app_name}/eval_results",
      response_model_exclude_none=True,
  )
  def list_eval_results(app_name: str) -> list[str]:
    """Lists all eval results for the given app."""
    return eval_set_results_manager.list_eval_set_results(app_name)
  @app.delete("/apps/{app_name}/users/{user_id}/sessions/{session_id}")
  async def delete_session(app_name: str, user_id: str, session_id: str):
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    await session_service.delete_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}",
      response_model_exclude_none=True,
  )
  async def load_artifact(
      app_name: str,
      user_id: str,
      session_id: str,
      artifact_name: str,
      version: Optional[int] = Query(None),
  ) -> Optional[types.Part]:
    app_name = agent_engine_id if agent_engine_id else app_name
    artifact = await artifact_service.load_artifact(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        filename=artifact_name,
        version=version,
    )
    if not artifact:
      raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions/{version_id}",
      response_model_exclude_none=True,
  )
  async def load_artifact_version(
      app_name: str,
      user_id: str,
      session_id: str,
      artifact_name: str,
      version_id: int,
  ) -> Optional[types.Part]:
    app_name = agent_engine_id if agent_engine_id else app_name
    artifact = await artifact_service.load_artifact(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        filename=artifact_name,
        version=version_id,
    )
    if not artifact:
      raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts",
      response_model_exclude_none=True,
  )
  async def list_artifact_names(
      app_name: str, user_id: str, session_id: str
  ) -> list[str]:
    app_name = agent_engine_id if agent_engine_id else app_name
    return await artifact_service.list_artifact_keys(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions",
      response_model_exclude_none=True,
  )
  async def list_artifact_versions(
      app_name: str, user_id: str, session_id: str, artifact_name: str
  ) -> list[int]:
    app_name = agent_engine_id if agent_engine_id else app_name
    return await artifact_service.list_versions(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        filename=artifact_name,
    )
  @app.delete(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}",
  )
  async def delete_artifact(
      app_name: str, user_id: str, session_id: str, artifact_name: str
  ):
    app_name = agent_engine_id if agent_engine_id else app_name
    await artifact_service.delete_artifact(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        filename=artifact_name,
    )
  @app.post("/run", response_model_exclude_none=True)
  async def agent_run(req: AgentRunRequest) -> list[Event]:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else req.app_name
    session = await session_service.get_session(
        app_name=app_name, user_id=req.user_id, session_id=req.session_id
    )
    if not session:
      raise HTTPException(status_code=404, detail="Session not found")
    runner = await _get_runner_async(req.app_name)
    events = [
        event
        async for event in runner.run_async(
            user_id=req.user_id,
            session_id=req.session_id,
            new_message=req.new_message,
        )
    ]
    logger.info("Generated %s events in agent run: %s", len(events), events)
    return events
  @app.post("/run_sse")
  async def agent_run_sse(req: AgentRunRequest) -> StreamingResponse:
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else req.app_name
    # SSE endpoint
    session = await session_service.get_session(
        app_name=app_name, user_id=req.user_id, session_id=req.session_id
    )
    if not session:
      raise HTTPException(status_code=404, detail="Session not found")
    # Convert the events to properly formatted SSE
    async def event_generator():
      try:
        stream_mode = StreamingMode.SSE if req.streaming else StreamingMode.NONE
        runner = await _get_runner_async(req.app_name)
        async for event in runner.run_async(
            user_id=req.user_id,
            session_id=req.session_id,
            new_message=req.new_message,
            run_config=RunConfig(streaming_mode=stream_mode),
        ):
          # Format as SSE data
          sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
          logger.info("Generated event in agent run streaming: %s", sse_event)
          yield f"data: {sse_event}\n\n"
      except Exception as e:
        logger.exception("Error in event_generator: %s", e)
        # You might want to yield an error event here
        yield f'data: {{"error": "{str(e)}"}}\n\n'
    # Returns a streaming response with the proper media type for SSE
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
  @app.get(
      "/apps/{app_name}/users/{user_id}/sessions/{session_id}/events/{event_id}/graph",
      response_model_exclude_none=True,
  )
  async def get_event_graph(
      app_name: str, user_id: str, session_id: str, event_id: str
  ):
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    session = await session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    session_events = session.events if session else []
    event = next((x for x in session_events if x.id == event_id), None)
    if not event:
      return {}
    from . import agent_graph
    function_calls = event.get_function_calls()
    function_responses = event.get_function_responses()
    root_agent = agent_loader.load_agent(app_name)
    dot_graph = None
    if function_calls:
      function_call_highlights = []
      for function_call in function_calls:
        from_name = event.author
        to_name = function_call.name
        function_call_highlights.append((from_name, to_name))
        dot_graph = await agent_graph.get_agent_graph(
            root_agent, function_call_highlights
        )
    elif function_responses:
      function_responses_highlights = []
      for function_response in function_responses:
        from_name = function_response.name
        to_name = event.author
        function_responses_highlights.append((from_name, to_name))
        dot_graph = await agent_graph.get_agent_graph(
            root_agent, function_responses_highlights
        )
    else:
      from_name = event.author
      to_name = ""
      dot_graph = await agent_graph.get_agent_graph(
          root_agent, [(from_name, to_name)]
      )
    if dot_graph and isinstance(dot_graph, graphviz.Digraph):
      return GetEventGraphResult(dot_src=dot_graph.source)
    else:
      return {}
  @app.websocket("/run_live")
  async def agent_live_run(
      websocket: WebSocket,
      app_name: str,
      user_id: str,
      session_id: str,
      modalities: List[Literal["TEXT", "AUDIO"]] = Query(
          default=["TEXT", "AUDIO"]
      ),  # Only allows "TEXT" or "AUDIO"
  ) -> None:
    await websocket.accept()
    # Connect to managed session if agent_engine_id is set.
    app_name = agent_engine_id if agent_engine_id else app_name
    session = await session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    if not session:
      # Accept first so that the client is aware of connection establishment,
      # then close with a specific code.
      await websocket.close(code=1002, reason="Session not found")
      return
    live_request_queue = LiveRequestQueue()
    async def forward_events():
      runner = await _get_runner_async(app_name)
      async for event in runner.run_live(
          session=session, live_request_queue=live_request_queue
      ):
        await websocket.send_text(
            event.model_dump_json(exclude_none=True, by_alias=True)
        )
    async def process_messages():
      try:
        while True:
          data = await websocket.receive_text()
          # Validate and send the received message to the live queue.
          live_request_queue.send(LiveRequest.model_validate_json(data))
      except ValidationError as ve:
        logger.error("Validation error in process_messages: %s", ve)
    # Run both tasks concurrently and cancel all if one fails.
    tasks = [
        asyncio.create_task(forward_events()),
        asyncio.create_task(process_messages()),
    ]
    done, pending = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_EXCEPTION
    )
    try:
      # This will re-raise any exception from the completed tasks.
      for task in done:
        task.result()
    except WebSocketDisconnect:
      logger.info("Client disconnected during process_messages.")
    except Exception as e:
      logger.exception("Error during live websocket communication: %s", e)
      traceback.print_exc()
      WEBSOCKET_INTERNAL_ERROR_CODE = 1011
      WEBSOCKET_MAX_BYTES_FOR_REASON = 123
      await websocket.close(
          code=WEBSOCKET_INTERNAL_ERROR_CODE,
          reason=str(e)[:WEBSOCKET_MAX_BYTES_FOR_REASON],
      )
    finally:
      for task in pending:
        task.cancel()
  async def _get_runner_async(app_name: str) -> Runner:
    """Returns the runner for the given app."""
    envs.load_dotenv_for_agent(os.path.basename(app_name), agents_dir)
    if app_name in runner_dict:
      return runner_dict[app_name]
    root_agent = agent_loader.load_agent(app_name)
    runner = Runner(
        app_name=agent_engine_id if agent_engine_id else app_name,
        agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
        memory_service=memory_service,
    )
    runner_dict[app_name] = runner
    return runner
  if web:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
    mimetypes.add_type("text/javascript", ".js", True)
    BASE_DIR = Path(__file__).parent.resolve()
    ANGULAR_DIST_PATH = BASE_DIR / "browser"
    @app.get("/")
    async def redirect_root_to_dev_ui():
      return RedirectResponse("/dev-ui/")
    @app.get("/dev-ui")
    async def redirect_dev_ui_add_slash():
      return RedirectResponse("/dev-ui/")
    app.mount(
        "/dev-ui/",
        StaticFiles(directory=ANGULAR_DIST_PATH, html=True),
        name="static",
    )
  return app
================================================
File: src/google/adk/cli/browser/index.html
================================================
<!doctype html>
<!--
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<html lang="en" data-beasties-container>
<head>
  <meta charset="utf-8">
  <title>Agent Development Kit Dev UI</title>
  <base href="./">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="adk_favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <style>@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWtE6F15M.woff2) format('woff2');unicode-range:U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWvU6F15M.woff2) format('woff2');unicode-range:U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWtU6F15M.woff2) format('woff2');unicode-range:U+1F00-1FFF;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWuk6F15M.woff2) format('woff2');unicode-range:U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWu06F15M.woff2) format('woff2');unicode-range:U+0307-0308, U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWxU6F15M.woff2) format('woff2');unicode-range:U+0302-0303, U+0305, U+0307-0308, U+0310, U+0312, U+0315, U+031A, U+0326-0327, U+032C, U+032F-0330, U+0332-0333, U+0338, U+033A, U+0346, U+034D, U+0391-03A1, U+03A3-03A9, U+03B1-03C9, U+03D1, U+03D5-03D6, U+03F0-03F1, U+03F4-03F5, U+2016-2017, U+2034-2038, U+203C, U+2040, U+2043, U+2047, U+2050, U+2057, U+205F, U+2070-2071, U+2074-208E, U+2090-209C, U+20D0-20DC, U+20E1, U+20E5-20EF, U+2100-2112, U+2114-2115, U+2117-2121, U+2123-214F, U+2190, U+2192, U+2194-21AE, U+21B0-21E5, U+21F1-21F2, U+21F4-2211, U+2213-2214, U+2216-22FF, U+2308-230B, U+2310, U+2319, U+231C-2321, U+2336-237A, U+237C, U+2395, U+239B-23B7, U+23D0, U+23DC-23E1, U+2474-2475, U+25AF, U+25B3, U+25B7, U+25BD, U+25C1, U+25CA, U+25CC, U+25FB, U+266D-266F, U+27C0-27FF, U+2900-2AFF, U+2B0E-2B11, U+2B30-2B4C, U+2BFE, U+3030, U+FF5B, U+FF5D, U+1D400-1D7FF, U+1EE00-1EEFF;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqW106F15M.woff2) format('woff2');unicode-range:U+0001-000C, U+000E-001F, U+007F-009F, U+20DD-20E0, U+20E2-20E4, U+2150-218F, U+2190, U+2192, U+2194-2199, U+21AF, U+21E6-21F0, U+21F3, U+2218-2219, U+2299, U+22C4-22C6, U+2300-243F, U+2440-244A, U+2460-24FF, U+25A0-27BF, U+2800-28FF, U+2921-2922, U+2981, U+29BF, U+29EB, U+2B00-2BFF, U+4DC0-4DFF, U+FFF9-FFFB, U+10140-1018E, U+10190-1019C, U+101A0, U+101D0-101FD, U+102E0-102FB, U+10E60-10E7E, U+1D2C0-1D2D3, U+1D2E0-1D37F, U+1F000-1F0FF, U+1F100-1F1AD, U+1F1E6-1F1FF, U+1F30D-1F30F, U+1F315, U+1F31C, U+1F31E, U+1F320-1F32C, U+1F336, U+1F378, U+1F37D, U+1F382, U+1F393-1F39F, U+1F3A7-1F3A8, U+1F3AC-1F3AF, U+1F3C2, U+1F3C4-1F3C6, U+1F3CA-1F3CE, U+1F3D4-1F3E0, U+1F3ED, U+1F3F1-1F3F3, U+1F3F5-1F3F7, U+1F408, U+1F415, U+1F41F, U+1F426, U+1F43F, U+1F441-1F442, U+1F444, U+1F446-1F449, U+1F44C-1F44E, U+1F453, U+1F46A, U+1F47D, U+1F4A3, U+1F4B0, U+1F4B3, U+1F4B9, U+1F4BB, U+1F4BF, U+1F4C8-1F4CB, U+1F4D6, U+1F4DA, U+1F4DF, U+1F4E3-1F4E6, U+1F4EA-1F4ED, U+1F4F7, U+1F4F9-1F4FB, U+1F4FD-1F4FE, U+1F503, U+1F507-1F50B, U+1F50D, U+1F512-1F513, U+1F53E-1F54A, U+1F54F-1F5FA, U+1F610, U+1F650-1F67F, U+1F687, U+1F68D, U+1F691, U+1F694, U+1F698, U+1F6AD, U+1F6B2, U+1F6B9-1F6BA, U+1F6BC, U+1F6C6-1F6CF, U+1F6D3-1F6D7, U+1F6E0-1F6EA, U+1F6F0-1F6F3, U+1F6F7-1F6FC, U+1F700-1F7FF, U+1F800-1F80B, U+1F810-1F847, U+1F850-1F859, U+1F860-1F887, U+1F890-1F8AD, U+1F8B0-1F8BB, U+1F8C0-1F8C1, U+1F900-1F90B, U+1F93B, U+1F946, U+1F984, U+1F996, U+1F9E9, U+1FA00-1FA6F, U+1FA70-1FA7C, U+1FA80-1FA89, U+1FA8F-1FAC6, U+1FACE-1FADC, U+1FADF-1FAE9, U+1FAF0-1FAF8, U+1FB00-1FBFF;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWtk6F15M.woff2) format('woff2');unicode-range:U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWt06F15M.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}@font-face{font-family:'Open Sans';font-style:italic;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWuU6F.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTSKmu1aB.woff2) format('woff2');unicode-range:U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTSumu1aB.woff2) format('woff2');unicode-range:U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTSOmu1aB.woff2) format('woff2');unicode-range:U+1F00-1FFF;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTSymu1aB.woff2) format('woff2');unicode-range:U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTS2mu1aB.woff2) format('woff2');unicode-range:U+0307-0308, U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTVOmu1aB.woff2) format('woff2');unicode-range:U+0302-0303, U+0305, U+0307-0308, U+0310, U+0312, U+0315, U+031A, U+0326-0327, U+032C, U+032F-0330, U+0332-0333, U+0338, U+033A, U+0346, U+034D, U+0391-03A1, U+03A3-03A9, U+03B1-03C9, U+03D1, U+03D5-03D6, U+03F0-03F1, U+03F4-03F5, U+2016-2017, U+2034-2038, U+203C, U+2040, U+2043, U+2047, U+2050, U+2057, U+205F, U+2070-2071, U+2074-208E, U+2090-209C, U+20D0-20DC, U+20E1, U+20E5-20EF, U+2100-2112, U+2114-2115, U+2117-2121, U+2123-214F, U+2190, U+2192, U+2194-21AE, U+21B0-21E5, U+21F1-21F2, U+21F4-2211, U+2213-2214, U+2216-22FF, U+2308-230B, U+2310, U+2319, U+231C-2321, U+2336-237A, U+237C, U+2395, U+239B-23B7, U+23D0, U+23DC-23E1, U+2474-2475, U+25AF, U+25B3, U+25B7, U+25BD, U+25C1, U+25CA, U+25CC, U+25FB, U+266D-266F, U+27C0-27FF, U+2900-2AFF, U+2B0E-2B11, U+2B30-2B4C, U+2BFE, U+3030, U+FF5B, U+FF5D, U+1D400-1D7FF, U+1EE00-1EEFF;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTUGmu1aB.woff2) format('woff2');unicode-range:U+0001-000C, U+000E-001F, U+007F-009F, U+20DD-20E0, U+20E2-20E4, U+2150-218F, U+2190, U+2192, U+2194-2199, U+21AF, U+21E6-21F0, U+21F3, U+2218-2219, U+2299, U+22C4-22C6, U+2300-243F, U+2440-244A, U+2460-24FF, U+25A0-27BF, U+2800-28FF, U+2921-2922, U+2981, U+29BF, U+29EB, U+2B00-2BFF, U+4DC0-4DFF, U+FFF9-FFFB, U+10140-1018E, U+10190-1019C, U+101A0, U+101D0-101FD, U+102E0-102FB, U+10E60-10E7E, U+1D2C0-1D2D3, U+1D2E0-1D37F, U+1F000-1F0FF, U+1F100-1F1AD, U+1F1E6-1F1FF, U+1F30D-1F30F, U+1F315, U+1F31C, U+1F31E, U+1F320-1F32C, U+1F336, U+1F378, U+1F37D, U+1F382, U+1F393-1F39F, U+1F3A7-1F3A8, U+1F3AC-1F3AF, U+1F3C2, U+1F3C4-1F3C6, U+1F3CA-1F3CE, U+1F3D4-1F3E0, U+1F3ED, U+1F3F1-1F3F3, U+1F3F5-1F3F7, U+1F408, U+1F415, U+1F41F, U+1F426, U+1F43F, U+1F441-1F442, U+1F444, U+1F446-1F449, U+1F44C-1F44E, U+1F453, U+1F46A, U+1F47D, U+1F4A3, U+1F4B0, U+1F4B3, U+1F4B9, U+1F4BB, U+1F4BF, U+1F4C8-1F4CB, U+1F4D6, U+1F4DA, U+1F4DF, U+1F4E3-1F4E6, U+1F4EA-1F4ED, U+1F4F7, U+1F4F9-1F4FB, U+1F4FD-1F4FE, U+1F503, U+1F507-1F50B, U+1F50D, U+1F512-1F513, U+1F53E-1F54A, U+1F54F-1F5FA, U+1F610, U+1F650-1F67F, U+1F687, U+1F68D, U+1F691, U+1F694, U+1F698, U+1F6AD, U+1F6B2, U+1F6B9-1F6BA, U+1F6BC, U+1F6C6-1F6CF, U+1F6D3-1F6D7, U+1F6E0-1F6EA, U+1F6F0-1F6F3, U+1F6F7-1F6FC, U+1F700-1F7FF, U+1F800-1F80B, U+1F810-1F847, U+1F850-1F859, U+1F860-1F887, U+1F890-1F8AD, U+1F8B0-1F8BB, U+1F8C0-1F8C1, U+1F900-1F90B, U+1F93B, U+1F946, U+1F984, U+1F996, U+1F9E9, U+1FA00-1FA6F, U+1FA70-1FA7C, U+1FA80-1FA89, U+1FA8F-1FAC6, U+1FACE-1FADC, U+1FADF-1FAE9, U+1FAF0-1FAF8, U+1FB00-1FBFF;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTSCmu1aB.woff2) format('woff2');unicode-range:U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTSGmu1aB.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/opensans/v40/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTS-muw.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}</style>
  <style>@font-face{font-family:'Material Icons';font-style:normal;font-weight:400;src:url(https://fonts.gstatic.com/s/materialicons/v143/flUhRq6tzZclQEJ-Vdg-IuiaDsNc.woff2) format('woff2');}.material-icons{font-family:'Material Icons';font-weight:normal;font-style:normal;font-size:24px;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-feature-settings:'liga';-webkit-font-smoothing:antialiased;}</style>
<style>html{color-scheme:dark}html{--mat-sys-background:light-dark(#fcf9f8, #131314);--mat-sys-error:light-dark(#ba1a1a, #ffb4ab);--mat-sys-error-container:light-dark(#ffdad6, #93000a);--mat-sys-inverse-on-surface:light-dark(#f3f0f0, #313030);--mat-sys-inverse-primary:light-dark(#c1c7cd, #595f65);--mat-sys-inverse-surface:light-dark(#313030, #e5e2e2);--mat-sys-on-background:light-dark(#1c1b1c, #e5e2e2);--mat-sys-on-error:light-dark(#ffffff, #690005);--mat-sys-on-error-container:light-dark(#410002, #ffdad6);--mat-sys-on-primary:light-dark(#ffffff, #2b3136);--mat-sys-on-primary-container:light-dark(#161c21, #dde3e9);--mat-sys-on-primary-fixed:light-dark(#161c21, #161c21);--mat-sys-on-primary-fixed-variant:light-dark(#41474d, #41474d);--mat-sys-on-secondary:light-dark(#ffffff, #003061);--mat-sys-on-secondary-container:light-dark(#001b3c, #d5e3ff);--mat-sys-on-secondary-fixed:light-dark(#001b3c, #001b3c);--mat-sys-on-secondary-fixed-variant:light-dark(#0f4784, #0f4784);--mat-sys-on-surface:light-dark(#1c1b1c, #e5e2e2);--mat-sys-on-surface-variant:light-dark(#44474a, #e1e2e6);--mat-sys-on-tertiary:light-dark(#ffffff, #2b3136);--mat-sys-on-tertiary-container:light-dark(#161c21, #dde3e9);--mat-sys-on-tertiary-fixed:light-dark(#161c21, #161c21);--mat-sys-on-tertiary-fixed-variant:light-dark(#41474d, #41474d);--mat-sys-outline:light-dark(#74777b, #8e9194);--mat-sys-outline-variant:light-dark(#c4c7ca, #44474a);--mat-sys-primary:light-dark(#595f65, #c1c7cd);--mat-sys-primary-container:light-dark(#dde3e9, #41474d);--mat-sys-primary-fixed:light-dark(#dde3e9, #dde3e9);--mat-sys-primary-fixed-dim:light-dark(#c1c7cd, #c1c7cd);--mat-sys-scrim:light-dark(#000000, #000000);--mat-sys-secondary:light-dark(#305f9d, #a7c8ff);--mat-sys-secondary-container:light-dark(#d5e3ff, #0f4784);--mat-sys-secondary-fixed:light-dark(#d5e3ff, #d5e3ff);--mat-sys-secondary-fixed-dim:light-dark(#a7c8ff, #a7c8ff);--mat-sys-shadow:light-dark(#000000, #000000);--mat-sys-surface:light-dark(#fcf9f8, #131314);--mat-sys-surface-bright:light-dark(#fcf9f8, #393939);--mat-sys-surface-container:light-dark(#f0eded, #201f20);--mat-sys-surface-container-high:light-dark(#eae7e7, #2a2a2a);--mat-sys-surface-container-highest:light-dark(#e5e2e2, #393939);--mat-sys-surface-container-low:light-dark(#f6f3f3, #1c1b1c);--mat-sys-surface-container-lowest:light-dark(#ffffff, #0e0e0e);--mat-sys-surface-dim:light-dark(#dcd9d9, #131314);--mat-sys-surface-tint:light-dark(#595f65, #c1c7cd);--mat-sys-surface-variant:light-dark(#e1e2e6, #44474a);--mat-sys-tertiary:light-dark(#595f65, #c1c7cd);--mat-sys-tertiary-container:light-dark(#dde3e9, #41474d);--mat-sys-tertiary-fixed:light-dark(#dde3e9, #dde3e9);--mat-sys-tertiary-fixed-dim:light-dark(#c1c7cd, #c1c7cd);--mat-sys-neutral-variant20:#2d3134;--mat-sys-neutral10:#1c1b1c}html{--mat-sys-level0:0px 0px 0px 0px rgba(0, 0, 0, .2), 0px 0px 0px 0px rgba(0, 0, 0, .14), 0px 0px 0px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level1:0px 2px 1px -1px rgba(0, 0, 0, .2), 0px 1px 1px 0px rgba(0, 0, 0, .14), 0px 1px 3px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level2:0px 3px 3px -2px rgba(0, 0, 0, .2), 0px 3px 4px 0px rgba(0, 0, 0, .14), 0px 1px 8px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level3:0px 3px 5px -1px rgba(0, 0, 0, .2), 0px 6px 10px 0px rgba(0, 0, 0, .14), 0px 1px 18px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level4:0px 5px 5px -3px rgba(0, 0, 0, .2), 0px 8px 10px 1px rgba(0, 0, 0, .14), 0px 3px 14px 2px rgba(0, 0, 0, .12)}html{--mat-sys-level5:0px 7px 8px -4px rgba(0, 0, 0, .2), 0px 12px 17px 2px rgba(0, 0, 0, .14), 0px 5px 22px 4px rgba(0, 0, 0, .12)}html{--mat-sys-corner-extra-large:28px;--mat-sys-corner-extra-large-top:28px 28px 0 0;--mat-sys-corner-extra-small:4px;--mat-sys-corner-extra-small-top:4px 4px 0 0;--mat-sys-corner-full:9999px;--mat-sys-corner-large:16px;--mat-sys-corner-large-end:0 16px 16px 0;--mat-sys-corner-large-start:16px 0 0 16px;--mat-sys-corner-large-top:16px 16px 0 0;--mat-sys-corner-medium:12px;--mat-sys-corner-none:0;--mat-sys-corner-small:8px}html{--mat-sys-dragged-state-layer-opacity:.16;--mat-sys-focus-state-layer-opacity:.12;--mat-sys-hover-state-layer-opacity:.08;--mat-sys-pressed-state-layer-opacity:.12}html{font-family:Google Sans,Helvetica Neue,sans-serif!important}body{height:100vh;margin:0}:root{--mat-sys-primary:black;--mdc-checkbox-selected-icon-color:white;--mat-sys-background:#131314;--mat-tab-header-active-label-text-color:#8AB4F8;--mat-tab-header-active-hover-label-text-color:#8AB4F8;--mat-tab-header-active-focus-label-text-color:#8AB4F8;--mat-tab-header-label-text-weight:500;--mdc-text-button-label-text-color:#89b4f8}:root{--mdc-dialog-container-color:#2b2b2f}:root{--mdc-dialog-subhead-color:white}:root{--mdc-circular-progress-active-indicator-color:#a8c7fa}:root{--mdc-circular-progress-size:80}</style><link rel="stylesheet" href="./styles-4VDSPQ37.css" media="print" onload="this.media='all'"><noscript><link rel="stylesheet" href="./styles-4VDSPQ37.css"></noscript></head>
<body>
  <app-root></app-root>
<script src="./polyfills-B6TNHZQ6.js" type="module"></script><script src="./main-LY4B7FVQ.js" type="module"></script></body>
</html>
================================================
File: src/google/adk/cli/browser/main-LY4B7FVQ.js
================================================
/**
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var Vv=Object.defineProperty,Wv=Object.defineProperties;var zv=Object.getOwnPropertyDescriptors;var $I=Object.getOwnPropertySymbols;var sf=Object.prototype.hasOwnProperty,af=Object.prototype.propertyIsEnumerable;var rf=(t,e,A)=>e in t?Vv(t,e,{enumerable:!0,configurable:!0,writable:!0,value:A}):t[e]=A,b=(t,e)=>{for(var A in e||={})sf.call(e,A)&&rf(t,A,e[A]);if($I)for(var A of $I(e))af.call(e,A)&&rf(t,A,e[A]);return t},uA=(t,e)=>Wv(t,zv(e));var Gc=(t,e)=>{var A={};for(var i in t)sf.call(t,i)&&e.indexOf(i)<0&&(A[i]=t[i]);if(t!=null&&$I)for(var i of $I(t))e.indexOf(i)<0&&af.call(t,i)&&(A[i]=t[i]);return A};var $e=(t,e,A)=>new Promise((i,o)=>{var n=s=>{try{r(A.next(s))}catch(a){o(a)}},g=s=>{try{r(A.throw(s))}catch(a){o(a)}},r=s=>s.done?i(s.value):Promise.resolve(s.value).then(n,g);r((A=A.apply(t,e)).next())});function Uc(t,e){return Object.is(t,e)}var Te=null,AC=!1,xc=1,yt=Symbol("SIGNAL");function WA(t){let e=Te;return Te=t,e}function Yc(){return Te}var Vg={version:0,lastCleanEpoch:0,dirty:!1,producerNode:void 0,producerLastReadVersion:void 0,producerIndexOfThis:void 0,nextProducerIndex:0,liveConsumerNode:void 0,liveConsumerIndexOfThis:void 0,consumerAllowSignalWrites:!1,consumerIsAlwaysLive:!1,kind:"unknown",producerMustRecompute:()=>!1,producerRecomputeValue:()=>{},consumerMarkedDirty:()=>{},consumerOnSignalRead:()=>{}};function vs(t){if(AC)throw new Error("");if(Te===null)return;Te.consumerOnSignalRead(t);let e=Te.nextProducerIndex++;if(nC(Te),e<Te.producerNode.length&&Te.producerNode[e]!==t&&Fs(Te)){let A=Te.producerNode[e];oC(A,Te.producerIndexOfThis[e])}Te.producerNode[e]!==t&&(Te.producerNode[e]=t,Te.producerIndexOfThis[e]=Fs(Te)?Cf(t,Te,e):0),Te.producerLastReadVersion[e]=t.version}function If(){xc++}function Jc(t){if(!(Fs(t)&&!t.dirty)&&!(!t.dirty&&t.lastCleanEpoch===xc)){if(!t.producerMustRecompute(t)&&!iC(t)){Kc(t);return}t.producerRecomputeValue(t),Kc(t)}}function Hc(t){if(t.liveConsumerNode===void 0)return;let e=AC;AC=!0;try{for(let A of t.liveConsumerNode)A.dirty||jv(A)}finally{AC=e}}function Tc(){return Te?.consumerAllowSignalWrites!==!1}function jv(t){t.dirty=!0,Hc(t),t.consumerMarkedDirty?.(t)}function Kc(t){t.dirty=!1,t.lastCleanEpoch=xc}function Ss(t){return t&&(t.nextProducerIndex=0),WA(t)}function tC(t,e){if(WA(e),!(!t||t.producerNode===void 0||t.producerIndexOfThis===void 0||t.producerLastReadVersion===void 0)){if(Fs(t))for(let A=t.nextProducerIndex;A<t.producerNode.length;A++)oC(t.producerNode[A],t.producerIndexOfThis[A]);for(;t.producerNode.length>t.nextProducerIndex;)t.producerNode.pop(),t.producerLastReadVersion.pop(),t.producerIndexOfThis.pop()}}function iC(t){nC(t);for(let e=0;e<t.producerNode.length;e++){let A=t.producerNode[e],i=t.producerLastReadVersion[e];if(i!==A.version||(Jc(A),i!==A.version))return!0}return!1}function Ns(t){if(nC(t),Fs(t))for(let e=0;e<t.producerNode.length;e++)oC(t.producerNode[e],t.producerIndexOfThis[e]);t.producerNode.length=t.producerLastReadVersion.length=t.producerIndexOfThis.length=0,t.liveConsumerNode&&(t.liveConsumerNode.length=t.liveConsumerIndexOfThis.length=0)}function Cf(t,e,A){if(Bf(t),t.liveConsumerNode.length===0&&Qf(t))for(let i=0;i<t.producerNode.length;i++)t.producerIndexOfThis[i]=Cf(t.producerNode[i],t,i);return t.liveConsumerIndexOfThis.push(A),t.liveConsumerNode.push(e)-1}function oC(t,e){if(Bf(t),t.liveConsumerNode.length===1&&Qf(t))for(let i=0;i<t.producerNode.length;i++)oC(t.producerNode[i],t.producerIndexOfThis[i]);let A=t.liveConsumerNode.length-1;if(t.liveConsumerNode[e]=t.liveConsumerNode[A],t.liveConsumerIndexOfThis[e]=t.liveConsumerIndexOfThis[A],t.liveConsumerNode.length--,t.liveConsumerIndexOfThis.length--,e<t.liveConsumerNode.length){let i=t.liveConsumerIndexOfThis[e],o=t.liveConsumerNode[e];nC(o),o.producerIndexOfThis[i]=e}}function Fs(t){return t.consumerIsAlwaysLive||(t?.liveConsumerNode?.length??0)>0}function nC(t){t.producerNode??=[],t.producerIndexOfThis??=[],t.producerLastReadVersion??=[]}function Bf(t){t.liveConsumerNode??=[],t.liveConsumerIndexOfThis??=[]}function Qf(t){return t.producerNode!==void 0}function gC(t,e){let A=Object.create(Xv);A.computation=t,e!==void 0&&(A.equal=e);let i=()=>{if(Jc(A),vs(A),A.value===eC)throw A.error;return A.value};return i[yt]=A,i}var Lc=Symbol("UNSET"),_c=Symbol("COMPUTING"),eC=Symbol("ERRORED"),Xv=uA(b({},Vg),{value:Lc,dirty:!0,error:null,equal:Uc,kind:"computed",producerMustRecompute(t){return t.value===Lc||t.value===_c},producerRecomputeValue(t){if(t.value===_c)throw new Error("Detected cycle in computations.");let e=t.value;t.value=_c;let A=Ss(t),i,o=!1;try{i=t.computation(),WA(null),o=e!==Lc&&e!==eC&&i!==eC&&t.equal(e,i)}catch(n){i=eC,t.error=n}finally{tC(t,A)}if(o){t.value=e;return}t.value=i,t.version++}});function $v(){throw new Error}var Ef=$v;function cf(t){Ef(t)}function Oc(t){Ef=t}var AS=null;function Pc(t,e){let A=Object.create(rC);A.value=t,e!==void 0&&(A.equal=e);let i=()=>(vs(A),A.value);return i[yt]=A,i}function Gs(t,e){Tc()||cf(t),t.equal(t.value,e)||(t.value=e,eS(t))}function Zc(t,e){Tc()||cf(t),Gs(t,e(t.value))}var rC=uA(b({},Vg),{equal:Uc,value:void 0,kind:"signal"});function eS(t){t.version++,If(),Hc(t),AS?.()}function qc(t){let e=WA(null);try{return t()}finally{WA(e)}}var Vc;function Ls(){return Vc}function Fo(t){let e=Vc;return Vc=t,e}var sC=Symbol("NotFound");function MA(t){return typeof t=="function"}function Wg(t){let A=t(i=>{Error.call(i),i.stack=new Error().stack});return A.prototype=Object.create(Error.prototype),A.prototype.constructor=A,A}var aC=Wg(t=>function(A){t(this),this.message=A?`${A.length} errors occurred during unsubscription:
${A.map((i,o)=>`${o+1}) ${i.toString()}`).join(`
  `)}`:"",this.name="UnsubscriptionError",this.errors=A});function Pn(t,e){if(t){let A=t.indexOf(e);0<=A&&t.splice(A,1)}}var GA=class t{constructor(e){this.initialTeardown=e,this.closed=!1,this._parentage=null,this._finalizers=null}unsubscribe(){let e;if(!this.closed){this.closed=!0;let{_parentage:A}=this;if(A)if(this._parentage=null,Array.isArray(A))for(let n of A)n.remove(this);else A.remove(this);let{initialTeardown:i}=this;if(MA(i))try{i()}catch(n){e=n instanceof aC?n.errors:[n]}let{_finalizers:o}=this;if(o){this._finalizers=null;for(let n of o)try{lf(n)}catch(g){e=e??[],g instanceof aC?e=[...e,...g.errors]:e.push(g)}}if(e)throw new aC(e)}}add(e){var A;if(e&&e!==this)if(this.closed)lf(e);else{if(e instanceof t){if(e.closed||e._hasParent(this))return;e._addParent(this)}(this._finalizers=(A=this._finalizers)!==null&&A!==void 0?A:[]).push(e)}}_hasParent(e){let{_parentage:A}=this;return A===e||Array.isArray(A)&&A.includes(e)}_addParent(e){let{_parentage:A}=this;this._parentage=Array.isArray(A)?(A.push(e),A):A?[A,e]:e}_removeParent(e){let{_parentage:A}=this;A===e?this._parentage=null:Array.isArray(A)&&Pn(A,e)}remove(e){let{_finalizers:A}=this;A&&Pn(A,e),e instanceof t&&e._removeParent(this)}};GA.EMPTY=(()=>{let t=new GA;return t.closed=!0,t})();var Wc=GA.EMPTY;function IC(t){return t instanceof GA||t&&"closed"in t&&MA(t.remove)&&MA(t.add)&&MA(t.unsubscribe)}function lf(t){MA(t)?t():t.unsubscribe()}var Di={onUnhandledError:null,onStoppedNotification:null,Promise:void 0,useDeprecatedSynchronousErrorHandling:!1,useDeprecatedNextContext:!1};var zg={setTimeout(t,e,...A){let{delegate:i}=zg;return i?.setTimeout?i.setTimeout(t,e,...A):setTimeout(t,e,...A)},clearTimeout(t){let{delegate:e}=zg;return(e?.clearTimeout||clearTimeout)(t)},delegate:void 0};function CC(t){zg.setTimeout(()=>{let{onUnhandledError:e}=Di;if(e)e(t);else throw t})}function _s(){}var df=zc("C",void 0,void 0);function hf(t){return zc("E",void 0,t)}function uf(t){return zc("N",t,void 0)}function zc(t,e,A){return{kind:t,value:e,error:A}}var Zn=null;function jg(t){if(Di.useDeprecatedSynchronousErrorHandling){let e=!Zn;if(e&&(Zn={errorThrown:!1,error:null}),t(),e){let{errorThrown:A,error:i}=Zn;if(Zn=null,A)throw i}}else t()}function mf(t){Di.useDeprecatedSynchronousErrorHandling&&Zn&&(Zn.errorThrown=!0,Zn.error=t)}var vo=class extends GA{constructor(e){super(),this.isStopped=!1,e?(this.destination=e,IC(e)&&e.add(this)):this.destination=rS}static create(e,A,i){return new So(e,A,i)}next(e){this.isStopped?Xc(uf(e),this):this._next(e)}error(e){this.isStopped?Xc(hf(e),this):(this.isStopped=!0,this._error(e))}complete(){this.isStopped?Xc(df,this):(this.isStopped=!0,this._complete())}unsubscribe(){this.closed||(this.isStopped=!0,super.unsubscribe(),this.destination=null)}_next(e){this.destination.next(e)}_error(e){try{this.destination.error(e)}finally{this.unsubscribe()}}_complete(){try{this.destination.complete()}finally{this.unsubscribe()}}},nS=Function.prototype.bind;function jc(t,e){return nS.call(t,e)}var $c=class{constructor(e){this.partialObserver=e}next(e){let{partialObserver:A}=this;if(A.next)try{A.next(e)}catch(i){BC(i)}}error(e){let{partialObserver:A}=this;if(A.error)try{A.error(e)}catch(i){BC(i)}else BC(e)}complete(){let{partialObserver:e}=this;if(e.complete)try{e.complete()}catch(A){BC(A)}}},So=class extends vo{constructor(e,A,i){super();let o;if(MA(e)||!e)o={next:e??void 0,error:A??void 0,complete:i??void 0};else{let n;this&&Di.useDeprecatedNextContext?(n=Object.create(e),n.unsubscribe=()=>this.unsubscribe(),o={next:e.next&&jc(e.next,n),error:e.error&&jc(e.error,n),complete:e.complete&&jc(e.complete,n)}):o=e}this.destination=new $c(o)}};function BC(t){Di.useDeprecatedSynchronousErrorHandling?mf(t):CC(t)}function gS(t){throw t}function Xc(t,e){let{onStoppedNotification:A}=Di;A&&zg.setTimeout(()=>A(t,e))}var rS={closed:!0,next:_s,error:gS,complete:_s};var Xg=typeof Symbol=="function"&&Symbol.observable||"@@observable";function ut(t){return t}function Al(...t){return el(t)}function el(t){return t.length===0?ut:t.length===1?t[0]:function(A){return t.reduce((i,o)=>o(i),A)}}var BA=(()=>{class t{constructor(A){A&&(this._subscribe=A)}lift(A){let i=new t;return i.source=this,i.operator=A,i}subscribe(A,i,o){let n=aS(A)?A:new So(A,i,o);return jg(()=>{let{operator:g,source:r}=this;n.add(g?g.call(n,r):r?this._subscribe(n):this._trySubscribe(n))}),n}_trySubscribe(A){try{return this._subscribe(A)}catch(i){A.error(i)}}forEach(A,i){return i=Df(i),new i((o,n)=>{let g=new So({next:r=>{try{A(r)}catch(s){n(s),g.unsubscribe()}},error:n,complete:o});this.subscribe(g)})}_subscribe(A){var i;return(i=this.source)===null||i===void 0?void 0:i.subscribe(A)}[Xg](){return this}pipe(...A){return el(A)(this)}toPromise(A){return A=Df(A),new A((i,o)=>{let n;this.subscribe(g=>n=g,g=>o(g),()=>i(n))})}}return t.create=e=>new t(e),t})();function Df(t){var e;return(e=t??Di.Promise)!==null&&e!==void 0?e:Promise}function sS(t){return t&&MA(t.next)&&MA(t.error)&&MA(t.complete)}function aS(t){return t&&t instanceof vo||sS(t)&&IC(t)}function tl(t){return MA(t?.lift)}function LA(t){return e=>{if(tl(e))return e.lift(function(A){try{return t(A,this)}catch(i){this.error(i)}});throw new TypeError("Unable to lift unknown Observable type")}}function SA(t,e,A,i,o){return new il(t,e,A,i,o)}var il=class extends vo{constructor(e,A,i,o,n,g){super(e),this.onFinalize=n,this.shouldUnsubscribe=g,this._next=A?function(r){try{A(r)}catch(s){e.error(s)}}:super._next,this._error=o?function(r){try{o(r)}catch(s){e.error(s)}finally{this.unsubscribe()}}:super._error,this._complete=i?function(){try{i()}catch(r){e.error(r)}finally{this.unsubscribe()}}:super._complete}unsubscribe(){var e;if(!this.shouldUnsubscribe||this.shouldUnsubscribe()){let{closed:A}=this;super.unsubscribe(),!A&&((e=this.onFinalize)===null||e===void 0||e.call(this))}}};function $g(){return LA((t,e)=>{let A=null;t._refCount++;let i=SA(e,void 0,void 0,void 0,()=>{if(!t||t._refCount<=0||0<--t._refCount){A=null;return}let o=t._connection,n=A;A=null,o&&(!n||o===n)&&o.unsubscribe(),e.unsubscribe()});t.subscribe(i),i.closed||(A=t.connect())})}var gn=class extends BA{constructor(e,A){super(),this.source=e,this.subjectFactory=A,this._subject=null,this._refCount=0,this._connection=null,tl(e)&&(this.lift=e.lift)}_subscribe(e){return this.getSubject().subscribe(e)}getSubject(){let e=this._subject;return(!e||e.isStopped)&&(this._subject=this.subjectFactory()),this._subject}_teardown(){this._refCount=0;let{_connection:e}=this;this._subject=this._connection=null,e?.unsubscribe()}connect(){let e=this._connection;if(!e){e=this._connection=new GA;let A=this.getSubject();e.add(this.source.subscribe(SA(A,void 0,()=>{this._teardown(),A.complete()},i=>{this._teardown(),A.error(i)},()=>this._teardown()))),e.closed&&(this._connection=null,e=GA.EMPTY)}return e}refCount(){return $g()(this)}};var ff=Wg(t=>function(){t(this),this.name="ObjectUnsubscribedError",this.message="object unsubscribed"});var U=(()=>{class t extends BA{constructor(){super(),this.closed=!1,this.currentObservers=null,this.observers=[],this.isStopped=!1,this.hasError=!1,this.thrownError=null}lift(A){let i=new Ar(this,this);return i.operator=A,i}_throwIfClosed(){if(this.closed)throw new ff}next(A){jg(()=>{if(this._throwIfClosed(),!this.isStopped){this.currentObservers||(this.currentObservers=Array.from(this.observers));for(let i of this.currentObservers)i.next(A)}})}error(A){jg(()=>{if(this._throwIfClosed(),!this.isStopped){this.hasError=this.isStopped=!0,this.thrownError=A;let{observers:i}=this;for(;i.length;)i.shift().error(A)}})}complete(){jg(()=>{if(this._throwIfClosed(),!this.isStopped){this.isStopped=!0;let{observers:A}=this;for(;A.length;)A.shift().complete()}})}unsubscribe(){this.isStopped=this.closed=!0,this.observers=this.currentObservers=null}get observed(){var A;return((A=this.observers)===null||A===void 0?void 0:A.length)>0}_trySubscribe(A){return this._throwIfClosed(),super._trySubscribe(A)}_subscribe(A){return this._throwIfClosed(),this._checkFinalizedStatuses(A),this._innerSubscribe(A)}_innerSubscribe(A){let{hasError:i,isStopped:o,observers:n}=this;return i||o?Wc:(this.currentObservers=null,n.push(A),new GA(()=>{this.currentObservers=null,Pn(n,A)}))}_checkFinalizedStatuses(A){let{hasError:i,thrownError:o,isStopped:n}=this;i?A.error(o):n&&A.complete()}asObservable(){let A=new BA;return A.source=this,A}}return t.create=(e,A)=>new Ar(e,A),t})(),Ar=class extends U{constructor(e,A){super(),this.destination=e,this.source=A}next(e){var A,i;(i=(A=this.destination)===null||A===void 0?void 0:A.next)===null||i===void 0||i.call(A,e)}error(e){var A,i;(i=(A=this.destination)===null||A===void 0?void 0:A.error)===null||i===void 0||i.call(A,e)}complete(){var e,A;(A=(e=this.destination)===null||e===void 0?void 0:e.complete)===null||A===void 0||A.call(e)}_subscribe(e){var A,i;return(i=(A=this.source)===null||A===void 0?void 0:A.subscribe(e))!==null&&i!==void 0?i:Wc}};var $A=class extends U{constructor(e){super(),this._value=e}get value(){return this.getValue()}_subscribe(e){let A=super._subscribe(e);return!A.closed&&e.next(this._value),A}getValue(){let{hasError:e,thrownError:A,_value:i}=this;if(e)throw A;return this._throwIfClosed(),i}next(e){super.next(this._value=e)}};var Ks={now(){return(Ks.delegate||Date).now()},delegate:void 0};var fi=class extends U{constructor(e=1/0,A=1/0,i=Ks){super(),this._bufferSize=e,this._windowTime=A,this._timestampProvider=i,this._buffer=[],this._infiniteTimeWindow=!0,this._infiniteTimeWindow=A===1/0,this._bufferSize=Math.max(1,e),this._windowTime=Math.max(1,A)}next(e){let{isStopped:A,_buffer:i,_infiniteTimeWindow:o,_timestampProvider:n,_windowTime:g}=this;A||(i.push(e),!o&&i.push(n.now()+g)),this._trimBuffer(),super.next(e)}_subscribe(e){this._throwIfClosed(),this._trimBuffer();let A=this._innerSubscribe(e),{_infiniteTimeWindow:i,_buffer:o}=this,n=o.slice();for(let g=0;g<n.length&&!e.closed;g+=i?1:2)e.next(n[g]);return this._checkFinalizedStatuses(e),A}_trimBuffer(){let{_bufferSize:e,_timestampProvider:A,_buffer:i,_infiniteTimeWindow:o}=this,n=(o?1:2)*e;if(e<1/0&&n<i.length&&i.splice(0,i.length-n),!o){let g=A.now(),r=0;for(let s=1;s<i.length&&i[s]<=g;s+=2)r=s;r&&i.splice(0,r+1)}}};var QC=class extends GA{constructor(e,A){super()}schedule(e,A=0){return this}};var Us={setInterval(t,e,...A){let{delegate:i}=Us;return i?.setInterval?i.setInterval(t,e,...A):setInterval(t,e,...A)},clearInterval(t){let{delegate:e}=Us;return(e?.clearInterval||clearInterval)(t)},delegate:void 0};var EC=class extends QC{constructor(e,A){super(e,A),this.scheduler=e,this.work=A,this.pending=!1}schedule(e,A=0){var i;if(this.closed)return this;this.state=e;let o=this.id,n=this.scheduler;return o!=null&&(this.id=this.recycleAsyncId(n,o,A)),this.pending=!0,this.delay=A,this.id=(i=this.id)!==null&&i!==void 0?i:this.requestAsyncId(n,this.id,A),this}requestAsyncId(e,A,i=0){return Us.setInterval(e.flush.bind(e,this),i)}recycleAsyncId(e,A,i=0){if(i!=null&&this.delay===i&&this.pending===!1)return A;A!=null&&Us.clearInterval(A)}execute(e,A){if(this.closed)return new Error("executing a cancelled action");this.pending=!1;let i=this._execute(e,A);if(i)return i;this.pending===!1&&this.id!=null&&(this.id=this.recycleAsyncId(this.scheduler,this.id,null))}_execute(e,A){let i=!1,o;try{this.work(e)}catch(n){i=!0,o=n||new Error("Scheduled action threw falsy error")}if(i)return this.unsubscribe(),o}unsubscribe(){if(!this.closed){let{id:e,scheduler:A}=this,{actions:i}=A;this.work=this.state=this.scheduler=null,this.pending=!1,Pn(i,this),e!=null&&(this.id=this.recycleAsyncId(A,e,null)),this.delay=null,super.unsubscribe()}}};var er=class t{constructor(e,A=t.now){this.schedulerActionCtor=e,this.now=A}schedule(e,A=0,i){return new this.schedulerActionCtor(this,e).schedule(i,A)}};er.now=Ks.now;var cC=class extends er{constructor(e,A=er.now){super(e,A),this.actions=[],this._active=!1}flush(e){let{actions:A}=this;if(this._active){A.push(e);return}let i;this._active=!0;do if(i=e.execute(e.state,e.delay))break;while(e=A.shift());if(this._active=!1,i){for(;e=A.shift();)e.unsubscribe();throw i}}};var xs=new cC(EC),pf=xs;var xe=new BA(t=>t.complete());function lC(t){return t&&MA(t.schedule)}function ol(t){return t[t.length-1]}function dC(t){return MA(ol(t))?t.pop():void 0}function Pi(t){return lC(ol(t))?t.pop():void 0}function wf(t,e){return typeof ol(t)=="number"?t.pop():e}function Mf(t,e,A,i){function o(n){return n instanceof A?n:new A(function(g){g(n)})}return new(A||(A=Promise))(function(n,g){function r(Q){try{a(i.next(Q))}catch(c){g(c)}}function s(Q){try{a(i.throw(Q))}catch(c){g(c)}}function a(Q){Q.done?n(Q.value):o(Q.value).then(r,s)}a((i=i.apply(t,e||[])).next())})}function yf(t){var e=typeof Symbol=="function"&&Symbol.iterator,A=e&&t[e],i=0;if(A)return A.call(t);if(t&&typeof t.length=="number")return{next:function(){return t&&i>=t.length&&(t=void 0),{value:t&&t[i++],done:!t}}};throw new TypeError(e?"Object is not iterable.":"Symbol.iterator is not defined.")}function qn(t){return this instanceof qn?(this.v=t,this):new qn(t)}function Rf(t,e,A){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var i=A.apply(t,e||[]),o,n=[];return o=Object.create((typeof AsyncIterator=="function"?AsyncIterator:Object).prototype),r("next"),r("throw"),r("return",g),o[Symbol.asyncIterator]=function(){return this},o;function g(m){return function(p){return Promise.resolve(p).then(m,c)}}function r(m,p){i[m]&&(o[m]=function(M){return new Promise(function(K,W){n.push([m,M,K,W])>1||s(m,M)})},p&&(o[m]=p(o[m])))}function s(m,p){try{a(i[m](p))}catch(M){f(n[0][3],M)}}function a(m){m.value instanceof qn?Promise.resolve(m.value.v).then(Q,c):f(n[0][2],m)}function Q(m){s("next",m)}function c(m){s("throw",m)}function f(m,p){m(p),n.shift(),n.length&&s(n[0][0],n[0][1])}}function kf(t){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var e=t[Symbol.asyncIterator],A;return e?e.call(t):(t=typeof yf=="function"?yf(t):t[Symbol.iterator](),A={},i("next"),i("throw"),i("return"),A[Symbol.asyncIterator]=function(){return this},A);function i(n){A[n]=t[n]&&function(g){return new Promise(function(r,s){g=t[n](g),o(r,s,g.done,g.value)})}}function o(n,g,r,s){Promise.resolve(s).then(function(a){n({value:a,done:r})},g)}}var tr=t=>t&&typeof t.length=="number"&&typeof t!="function";function hC(t){return MA(t?.then)}function uC(t){return MA(t[Xg])}function mC(t){return Symbol.asyncIterator&&MA(t?.[Symbol.asyncIterator])}function DC(t){return new TypeError(`You provided ${t!==null&&typeof t=="object"?"an invalid object":`'${t}'`} where a stream was expected. You can provide an Observable, Promise, ReadableStream, Array, AsyncIterable, or Iterable.`)}function IS(){return typeof Symbol!="function"||!Symbol.iterator?"@@iterator":Symbol.iterator}var fC=IS();function pC(t){return MA(t?.[fC])}function wC(t){return Rf(this,arguments,function*(){let A=t.getReader();try{for(;;){let{value:i,done:o}=yield qn(A.read());if(o)return yield qn(void 0);yield yield qn(i)}}finally{A.releaseLock()}})}function yC(t){return MA(t?.getReader)}function ne(t){if(t instanceof BA)return t;if(t!=null){if(uC(t))return CS(t);if(tr(t))return BS(t);if(hC(t))return QS(t);if(mC(t))return bf(t);if(pC(t))return ES(t);if(yC(t))return cS(t)}throw DC(t)}function CS(t){return new BA(e=>{let A=t[Xg]();if(MA(A.subscribe))return A.subscribe(e);throw new TypeError("Provided object does not correctly implement Symbol.observable")})}function BS(t){return new BA(e=>{for(let A=0;A<t.length&&!e.closed;A++)e.next(t[A]);e.complete()})}function QS(t){return new BA(e=>{t.then(A=>{e.closed||(e.next(A),e.complete())},A=>e.error(A)).then(null,CC)})}function ES(t){return new BA(e=>{for(let A of t)if(e.next(A),e.closed)return;e.complete()})}function bf(t){return new BA(e=>{lS(t,e).catch(A=>e.error(A))})}function cS(t){return bf(wC(t))}function lS(t,e){var A,i,o,n;return Mf(this,void 0,void 0,function*(){try{for(A=kf(t);i=yield A.next(),!i.done;){let g=i.value;if(e.next(g),e.closed)return}}catch(g){o={error:g}}finally{try{i&&!i.done&&(n=A.return)&&(yield n.call(A))}finally{if(o)throw o.error}}e.complete()})}function Mt(t,e,A,i=0,o=!1){let n=e.schedule(function(){A(),o?t.add(this.schedule(null,i)):this.unsubscribe()},i);if(t.add(n),!o)return n}function MC(t,e=0){return LA((A,i)=>{A.subscribe(SA(i,o=>Mt(i,t,()=>i.next(o),e),()=>Mt(i,t,()=>i.complete(),e),o=>Mt(i,t,()=>i.error(o),e)))})}function RC(t,e=0){return LA((A,i)=>{i.add(t.schedule(()=>A.subscribe(i),e))})}function Ff(t,e){return ne(t).pipe(RC(e),MC(e))}function vf(t,e){return ne(t).pipe(RC(e),MC(e))}function Sf(t,e){return new BA(A=>{let i=0;return e.schedule(function(){i===t.length?A.complete():(A.next(t[i++]),A.closed||this.schedule())})})}function Nf(t,e){return new BA(A=>{let i;return Mt(A,e,()=>{i=t[fC](),Mt(A,e,()=>{let o,n;try{({value:o,done:n}=i.next())}catch(g){A.error(g);return}n?A.complete():A.next(o)},0,!0)}),()=>MA(i?.return)&&i.return()})}function kC(t,e){if(!t)throw new Error("Iterable cannot be null");return new BA(A=>{Mt(A,e,()=>{let i=t[Symbol.asyncIterator]();Mt(A,e,()=>{i.next().then(o=>{o.done?A.complete():A.next(o.value)})},0,!0)})})}function Gf(t,e){return kC(wC(t),e)}function Lf(t,e){if(t!=null){if(uC(t))return Ff(t,e);if(tr(t))return Sf(t,e);if(hC(t))return vf(t,e);if(mC(t))return kC(t,e);if(pC(t))return Nf(t,e);if(yC(t))return Gf(t,e)}throw DC(t)}function se(t,e){return e?Lf(t,e):ne(t)}function iA(...t){let e=Pi(t);return se(t,e)}function rn(t,e){let A=MA(t)?t:()=>t,i=o=>o.error(A());return new BA(e?o=>e.schedule(i,0,o):i)}function sn(t){return!!t&&(t instanceof BA||MA(t.lift)&&MA(t.subscribe))}var No=Wg(t=>function(){t(this),this.name="EmptyError",this.message="no elements in sequence"});function _f(t){return t instanceof Date&&!isNaN(t)}function sA(t,e){return LA((A,i)=>{let o=0;A.subscribe(SA(i,n=>{i.next(t.call(e,n,o++))}))})}var{isArray:dS}=Array;function hS(t,e){return dS(e)?t(...e):t(e)}function ir(t){return sA(e=>hS(t,e))}var{isArray:uS}=Array,{getPrototypeOf:mS,prototype:DS,keys:fS}=Object;function bC(t){if(t.length===1){let e=t[0];if(uS(e))return{args:e,keys:null};if(pS(e)){let A=fS(e);return{args:A.map(i=>e[i]),keys:A}}}return{args:t,keys:null}}function pS(t){return t&&typeof t=="object"&&mS(t)===DS}function FC(t,e){return t.reduce((A,i,o)=>(A[i]=e[o],A),{})}function Rt(...t){let e=Pi(t),A=dC(t),{args:i,keys:o}=bC(t);if(i.length===0)return se([],e);let n=new BA(wS(i,e,o?g=>FC(o,g):ut));return A?n.pipe(ir(A)):n}function wS(t,e,A=ut){return i=>{Kf(e,()=>{let{length:o}=t,n=new Array(o),g=o,r=o;for(let s=0;s<o;s++)Kf(e,()=>{let a=se(t[s],e),Q=!1;a.subscribe(SA(i,c=>{n[s]=c,Q||(Q=!0,r--),r||i.next(A(n.slice()))},()=>{--g||i.complete()}))},i)},i)}}function Kf(t,e,A){t?Mt(A,t,e):e()}function Uf(t,e,A,i,o,n,g,r){let s=[],a=0,Q=0,c=!1,f=()=>{c&&!s.length&&!a&&e.complete()},m=M=>a<i?p(M):s.push(M),p=M=>{n&&e.next(M),a++;let K=!1;ne(A(M,Q++)).subscribe(SA(e,W=>{o?.(W),n?m(W):e.next(W)},()=>{K=!0},void 0,()=>{if(K)try{for(a--;s.length&&a<i;){let W=s.shift();g?Mt(e,g,()=>p(W)):p(W)}f()}catch(W){e.error(W)}}))};return t.subscribe(SA(e,m,()=>{c=!0,f()})),()=>{r?.()}}function ve(t,e,A=1/0){return MA(e)?ve((i,o)=>sA((n,g)=>e(i,n,o,g))(ne(t(i,o))),A):(typeof e=="number"&&(A=e),LA((i,o)=>Uf(i,o,t,A)))}function an(t=1/0){return ve(ut,t)}function xf(){return an(1)}function In(...t){return xf()(se(t,Pi(t)))}function Zi(t){return new BA(e=>{ne(t()).subscribe(e)})}function Ys(...t){let e=dC(t),{args:A,keys:i}=bC(t),o=new BA(n=>{let{length:g}=A;if(!g){n.complete();return}let r=new Array(g),s=g,a=g;for(let Q=0;Q<g;Q++){let c=!1;ne(A[Q]).subscribe(SA(n,f=>{c||(c=!0,a--),r[Q]=f},()=>s--,void 0,()=>{(!s||!c)&&(a||n.next(i?FC(i,r):r),n.complete())}))}});return e?o.pipe(ir(e)):o}var yS=["addListener","removeListener"],MS=["addEventListener","removeEventListener"],RS=["on","off"];function Js(t,e,A,i){if(MA(A)&&(i=A,A=void 0),i)return Js(t,e,A).pipe(ir(i));let[o,n]=FS(t)?MS.map(g=>r=>t[g](e,r,A)):kS(t)?yS.map(Yf(t,e)):bS(t)?RS.map(Yf(t,e)):[];if(!o&&tr(t))return ve(g=>Js(g,e,A))(ne(t));if(!o)throw new TypeError("Invalid event target");return new BA(g=>{let r=(...s)=>g.next(1<s.length?s:s[0]);return o(r),()=>n(r)})}function Yf(t,e){return A=>i=>t[A](e,i)}function kS(t){return MA(t.addListener)&&MA(t.removeListener)}function bS(t){return MA(t.on)&&MA(t.off)}function FS(t){return MA(t.addEventListener)&&MA(t.removeEventListener)}function Vn(t=0,e,A=pf){let i=-1;return e!=null&&(lC(e)?A=e:i=e),new BA(o=>{let n=_f(t)?+t-A.now():t;n<0&&(n=0);let g=0;return A.schedule(function(){o.closed||(o.next(g++),0<=i?this.schedule(void 0,i):o.complete())},n)})}function ye(...t){let e=Pi(t),A=wf(t,1/0),i=t;return i.length?i.length===1?ne(i[0]):an(A)(se(i,e)):xe}function kA(t,e){return LA((A,i)=>{let o=0;A.subscribe(SA(i,n=>t.call(e,n,o++)&&i.next(n)))})}function Jf(t){return LA((e,A)=>{let i=!1,o=null,n=null,g=!1,r=()=>{if(n?.unsubscribe(),n=null,i){i=!1;let a=o;o=null,A.next(a)}g&&A.complete()},s=()=>{n=null,g&&A.complete()};e.subscribe(SA(A,a=>{i=!0,o=a,n||ne(t(a)).subscribe(n=SA(A,r,s))},()=>{g=!0,(!i||!n||n.closed)&&A.complete()}))})}function or(t,e=xs){return Jf(()=>Vn(t,e))}function Oe(t){return LA((e,A)=>{let i=null,o=!1,n;i=e.subscribe(SA(A,void 0,void 0,g=>{n=ne(t(g,Oe(t)(e))),i?(i.unsubscribe(),i=null,n.subscribe(A)):o=!0})),o&&(i.unsubscribe(),i=null,n.subscribe(A))})}function Hf(t,e,A,i,o){return(n,g)=>{let r=A,s=e,a=0;n.subscribe(SA(g,Q=>{let c=a++;s=r?t(s,Q,c):(r=!0,Q),i&&g.next(s)},o&&(()=>{r&&g.next(s),g.complete()})))}}function qi(t,e){return MA(e)?ve(t,e,1):ve(t,1)}function pi(t,e=xs){return LA((A,i)=>{let o=null,n=null,g=null,r=()=>{if(o){o.unsubscribe(),o=null;let a=n;n=null,i.next(a)}};function s(){let a=g+t,Q=e.now();if(Q<a){o=this.schedule(void 0,a-Q),i.add(o);return}r()}A.subscribe(SA(i,a=>{n=a,g=e.now(),o||(o=e.schedule(s,t),i.add(o))},()=>{r(),i.complete()},void 0,()=>{n=o=null}))})}function Cn(t){return LA((e,A)=>{let i=!1;e.subscribe(SA(A,o=>{i=!0,A.next(o)},()=>{i||A.next(t),A.complete()}))})}function ue(t){return t<=0?()=>xe:LA((e,A)=>{let i=0;e.subscribe(SA(A,o=>{++i<=t&&(A.next(o),t<=i&&A.complete())}))})}function nr(t){return sA(()=>t)}function wi(t,e=ut){return t=t??vS,LA((A,i)=>{let o,n=!0;A.subscribe(SA(i,g=>{let r=e(g);(n||!t(o,r))&&(n=!1,o=r,i.next(g))}))})}function vS(t,e){return t===e}function vC(t=SS){return LA((e,A)=>{let i=!1;e.subscribe(SA(A,o=>{i=!0,A.next(o)},()=>i?A.complete():A.error(t())))})}function SS(){return new No}function Vi(t){return LA((e,A)=>{try{e.subscribe(A)}finally{A.add(t)}})}function Wi(t,e){let A=arguments.length>=2;return i=>i.pipe(t?kA((o,n)=>t(o,n,i)):ut,ue(1),A?Cn(e):vC(()=>new No))}function gr(t){return t<=0?()=>xe:LA((e,A)=>{let i=[];e.subscribe(SA(A,o=>{i.push(o),t<i.length&&i.shift()},()=>{for(let o of i)A.next(o);A.complete()},void 0,()=>{i=null}))})}function nl(t,e){let A=arguments.length>=2;return i=>i.pipe(t?kA((o,n)=>t(o,n,i)):ut,gr(1),A?Cn(e):vC(()=>new No))}function SC(){return LA((t,e)=>{let A,i=!1;t.subscribe(SA(e,o=>{let n=A;A=o,i&&e.next([n,o]),i=!0}))})}function gl(t,e){return LA(Hf(t,e,arguments.length>=2,!0))}function Hs(t={}){let{connector:e=()=>new U,resetOnError:A=!0,resetOnComplete:i=!0,resetOnRefCountZero:o=!0}=t;return n=>{let g,r,s,a=0,Q=!1,c=!1,f=()=>{r?.unsubscribe(),r=void 0},m=()=>{f(),g=s=void 0,Q=c=!1},p=()=>{let M=g;m(),M?.unsubscribe()};return LA((M,K)=>{a++,!c&&!Q&&f();let W=s=s??e();K.add(()=>{a--,a===0&&!c&&!Q&&(r=rl(p,o))}),W.subscribe(K),!g&&a>0&&(g=new So({next:DA=>W.next(DA),error:DA=>{c=!0,f(),r=rl(m,A,DA),W.error(DA)},complete:()=>{Q=!0,f(),r=rl(m,i),W.complete()}}),ne(M).subscribe(g))})(n)}}function rl(t,e,...A){if(e===!0){t();return}if(e===!1)return;let i=new So({next:()=>{i.unsubscribe(),t()}});return ne(e(...A)).subscribe(i)}function Go(t,e,A){let i,o=!1;return t&&typeof t=="object"?{bufferSize:i=1/0,windowTime:e=1/0,refCount:o=!1,scheduler:A}=t:i=t??1/0,Hs({connector:()=>new fi(i,e,A),resetOnError:!0,resetOnComplete:!1,resetOnRefCountZero:o})}function Wn(t){return kA((e,A)=>t<=A)}function Me(...t){let e=Pi(t);return LA((A,i)=>{(e?In(t,A,e):In(t,A)).subscribe(i)})}function Ie(t,e){return LA((A,i)=>{let o=null,n=0,g=!1,r=()=>g&&!o&&i.complete();A.subscribe(SA(i,s=>{o?.unsubscribe();let a=0,Q=n++;ne(t(s,Q)).subscribe(o=SA(i,c=>i.next(e?e(s,c,Q,a++):c),()=>{o=null,r()}))},()=>{g=!0,r()}))})}function pA(t){return LA((e,A)=>{ne(t).subscribe(SA(A,()=>A.complete(),_s)),!A.closed&&e.subscribe(A)})}function sl(t,e=!1){return LA((A,i)=>{let o=0;A.subscribe(SA(i,n=>{let g=t(n,o++);(g||e)&&i.next(n),!g&&i.complete()}))})}function Ce(t,e,A){let i=MA(t)||e||A?{next:t,error:e,complete:A}:t;return i?LA((o,n)=>{var g;(g=i.subscribe)===null||g===void 0||g.call(i);let r=!0;o.subscribe(SA(n,s=>{var a;(a=i.next)===null||a===void 0||a.call(i,s),n.next(s)},()=>{var s;r=!1,(s=i.complete)===null||s===void 0||s.call(i),n.complete()},s=>{var a;r=!1,(a=i.error)===null||a===void 0||a.call(i,s),n.error(s)},()=>{var s,a;r&&((s=i.unsubscribe)===null||s===void 0||s.call(i)),(a=i.finalize)===null||a===void 0||a.call(i)}))}):ut}var Lp="https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss",H=class extends Error{code;constructor(e,A){super(Sd(e,A)),this.code=e}};function NS(t){return`NG0${Math.abs(t)}`}function Sd(t,e){return`${NS(t)}${e?": "+e:""}`}var _p=Symbol("InputSignalNode#UNSET"),GS=uA(b({},rC),{transformFn:void 0,applyValueToInputSignal(t,e){Gs(t,e)}});function Kp(t,e){let A=Object.create(GS);A.value=t,A.transformFn=e?.transform;function i(){if(vs(A),A.value===_p){let o=null;throw new H(-950,o)}return A.value}return i[yt]=A,i}function ea(t){return{toString:t}.toString()}var NC="__parameters__";function LS(t){return function(...A){if(t){let i=t(...A);for(let o in i)this[o]=i[o]}}}function Up(t,e,A){return ea(()=>{let i=LS(e);function o(...n){if(this instanceof o)return i.apply(this,n),this;let g=new o(...n);return r.annotation=g,r;function r(s,a,Q){let c=s.hasOwnProperty(NC)?s[NC]:Object.defineProperty(s,NC,{value:[]})[NC];for(;c.length<=Q;)c.push(null);return(c[Q]=c[Q]||[]).push(g),s}}return o.prototype.ngMetadataName=t,o.annotationCls=o,o})}var Ft=globalThis;function Be(t){for(let e in t)if(t[e]===Be)return e;throw Error("Could not find renamed property on target object.")}function _S(t,e){for(let A in e)e.hasOwnProperty(A)&&!t.hasOwnProperty(A)&&(t[A]=e[A])}function bt(t){if(typeof t=="string")return t;if(Array.isArray(t))return`[${t.map(bt).join(", ")}]`;if(t==null)return""+t;let e=t.overriddenName||t.name;if(e)return`${e}`;let A=t.toString();if(A==null)return""+A;let i=A.indexOf(`
`);return i>=0?A.slice(0,i):A}function pl(t,e){return t?e?`${t} ${e}`:t:e||""}var KS=Be({__forward_ref__:Be});function ot(t){return t.__forward_ref__=ot,t.toString=function(){return bt(this())},t}function it(t){return xp(t)?t():t}function xp(t){return typeof t=="function"&&t.hasOwnProperty(KS)&&t.__forward_ref__===ot}function S(t){return{token:t.token,providedIn:t.providedIn||null,factory:t.factory,value:void 0}}function j(t){return{providers:t.providers||[],imports:t.imports||[]}}function mB(t){return Tf(t,Jp)||Tf(t,Hp)}function Yp(t){return mB(t)!==null}function Tf(t,e){return t.hasOwnProperty(e)?t[e]:null}function US(t){let e=t&&(t[Jp]||t[Hp]);return e||null}function Of(t){return t&&(t.hasOwnProperty(Pf)||t.hasOwnProperty(xS))?t[Pf]:null}var Jp=Be({\u0275prov:Be}),Pf=Be({\u0275inj:Be}),Hp=Be({ngInjectableDef:Be}),xS=Be({ngInjectorDef:Be}),F=class{_desc;ngMetadataName="InjectionToken";\u0275prov;constructor(e,A){this._desc=e,this.\u0275prov=void 0,typeof A=="number"?this.__NG_ELEMENT_ID__=A:A!==void 0&&(this.\u0275prov=S({token:this,providedIn:A.providedIn||"root",factory:A.factory}))}get multi(){return this}toString(){return`InjectionToken ${this._desc}`}};function Tp(t){return t&&!!t.\u0275providers}var YS=Be({\u0275cmp:Be}),JS=Be({\u0275dir:Be}),HS=Be({\u0275pipe:Be}),TS=Be({\u0275mod:Be}),OC=Be({\u0275fac:Be}),Zs=Be({__NG_ELEMENT_ID__:Be}),Zf=Be({__NG_ENV_ID__:Be});function ta(t){return typeof t=="string"?t:t==null?"":String(t)}function OS(t){return typeof t=="function"?t.name||t.toString():typeof t=="object"&&t!=null&&typeof t.type=="function"?t.type.name||t.type.toString():ta(t)}function Op(t,e){throw new H(-200,t)}function Nd(t,e){throw new H(-201,!1)}var zA=function(t){return t[t.Default=0]="Default",t[t.Host=1]="Host",t[t.Self=2]="Self",t[t.SkipSelf=4]="SkipSelf",t[t.Optional=8]="Optional",t}(zA||{}),wl;function Pp(){return wl}function kt(t){let e=wl;return wl=t,e}function Zp(t,e,A){let i=mB(t);if(i&&i.providedIn=="root")return i.value===void 0?i.value=i.factory():i.value;if(A&zA.Optional)return null;if(e!==void 0)return e;Nd(t,"Injector")}var PS={},zn=PS,yl="__NG_DI_FLAG__",PC=class{injector;constructor(e){this.injector=e}retrieve(e,A){let i=A;return this.injector.get(e,i.optional?sC:zn,i)}},ZC="ngTempTokenPath",ZS="ngTokenPath",qS=/\n/gm,VS="\u0275",qf="__source";function WS(t,e=zA.Default){if(Ls()===void 0)throw new H(-203,!1);if(Ls()===null)return Zp(t,void 0,e);{let A=Ls(),i;return A instanceof PC?i=A.injector:i=A,i.get(t,e&zA.Optional?null:void 0,e)}}function Z(t,e=zA.Default){return(Pp()||WS)(it(t),e)}function B(t,e=zA.Default){return Z(t,DB(e))}function DB(t){return typeof t>"u"||typeof t=="number"?t:0|(t.optional&&8)|(t.host&&1)|(t.self&&2)|(t.skipSelf&&4)}function Ml(t){let e=[];for(let A=0;A<t.length;A++){let i=it(t[A]);if(Array.isArray(i)){if(i.length===0)throw new H(900,!1);let o,n=zA.Default;for(let g=0;g<i.length;g++){let r=i[g],s=zS(r);typeof s=="number"?s===-1?o=r.token:n|=s:o=r}e.push(Z(o,n))}else e.push(Z(i))}return e}function qp(t,e){return t[yl]=e,t.prototype[yl]=e,t}function zS(t){return t[yl]}function jS(t,e,A,i){let o=t[ZC];throw e[qf]&&o.unshift(e[qf]),t.message=XS(`
`+t.message,o,A,i),t[ZS]=o,t[ZC]=null,t}function XS(t,e,A,i=null){t=t&&t.charAt(0)===`
`&&t.charAt(1)==VS?t.slice(2):t;let o=bt(e);if(Array.isArray(e))o=e.map(bt).join(" -> ");else if(typeof e=="object"){let n=[];for(let g in e)if(e.hasOwnProperty(g)){let r=e[g];n.push(g+":"+(typeof r=="string"?JSON.stringify(r):bt(r)))}o=`{${n.join(", ")}}`}return`${A}${i?"("+i+")":""}[${o}]: ${t.replace(qS,`
        --mat-mdc-form-field-label-transform,
        ${ZT} translateX(${p})
    )`;let M=r+s+a+Q;this._elementRef.nativeElement.style.setProperty("--mat-form-field-notch-max-width",`calc(100% - ${M}px)`)}_isAttachedToDom(){let A=this._elementRef.nativeElement;if(A.getRootNode){let i=A.getRootNode();return i&&i!==A}return document.documentElement.contains(A)}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["mat-form-field"]],contentQueries:function(i,o,n){if(i&1&&(p0(n,o._labelChild,LE,5),XA(n,dI,5),XA(n,JT,5),XA(n,Yk,5),XA(n,YT,5),XA(n,Nk,5)),i&2){w0();let g;$(g=AA())&&(o._formFieldControl=g.first),$(g=AA())&&(o._prefixChildren=g),$(g=AA())&&(o._suffixChildren=g),$(g=AA())&&(o._errorChildren=g),$(g=AA())&&(o._hintChildren=g)}},viewQuery:function(i,o){if(i&1&&(QA(lT,5),QA(dT,5),QA(hT,5),QA(uT,5),QA(mT,5),QA(Gk,5),QA(Kk,5),QA(_k,5)),i&2){let n;$(n=AA())&&(o._textField=n.first),$(n=AA())&&(o._iconPrefixContainer=n.first),$(n=AA())&&(o._textPrefixContainer=n.first),$(n=AA())&&(o._iconSuffixContainer=n.first),$(n=AA())&&(o._textSuffixContainer=n.first),$(n=AA())&&(o._floatingLabel=n.first),$(n=AA())&&(o._notchedOutline=n.first),$(n=AA())&&(o._lineRipple=n.first)}},hostAttrs:[1,"mat-mdc-form-field"],hostVars:42,hostBindings:function(i,o){i&2&&nA("mat-mdc-form-field-label-always-float",o._shouldAlwaysFloat())("mat-mdc-form-field-has-icon-prefix",o._hasIconPrefix)("mat-mdc-form-field-has-icon-suffix",o._hasIconSuffix)("mat-form-field-invalid",o._control.errorState)("mat-form-field-disabled",o._control.disabled)("mat-form-field-autofilled",o._control.autofilled)("mat-form-field-no-animations",o._animationMode==="NoopAnimations")("mat-form-field-appearance-fill",o.appearance=="fill")("mat-form-field-appearance-outline",o.appearance=="outline")("mat-form-field-hide-placeholder",o._hasFloatingLabel()&&!o._shouldLabelFloat())("mat-focused",o._control.focused)("mat-primary",o.color!=="accent"&&o.color!=="warn")("mat-accent",o.color==="accent")("mat-warn",o.color==="warn")("ng-untouched",o._shouldForward("untouched"))("ng-touched",o._shouldForward("touched"))("ng-pristine",o._shouldForward("pristine"))("ng-dirty",o._shouldForward("dirty"))("ng-valid",o._shouldForward("valid"))("ng-invalid",o._shouldForward("invalid"))("ng-pending",o._shouldForward("pending"))},inputs:{hideRequiredMarker:"hideRequiredMarker",color:"color",floatLabel:"floatLabel",appearance:"appearance",subscriptSizing:"subscriptSizing",hintLabel:"hintLabel"},exportAs:["matFormField"],features:[FA([{provide:hI,useExisting:t},{provide:Hk,useExisting:t}])],ngContentSelectors:fT,decls:18,vars:21,consts:[["labelTemplate",""],["textField",""],["iconPrefixContainer",""],["textPrefixContainer",""],["textSuffixContainer",""],["iconSuffixContainer",""],[1,"mat-mdc-text-field-wrapper","mdc-text-field",3,"click"],[1,"mat-mdc-form-field-focus-overlay"],[1,"mat-mdc-form-field-flex"],["matFormFieldNotchedOutline","",3,"matFormFieldNotchedOutlineOpen"],[1,"mat-mdc-form-field-icon-prefix"],[1,"mat-mdc-form-field-text-prefix"],[1,"mat-mdc-form-field-infix"],[3,"ngTemplateOutlet"],[1,"mat-mdc-form-field-text-suffix"],[1,"mat-mdc-form-field-icon-suffix"],["matFormFieldLineRipple",""],[1,"mat-mdc-form-field-subscript-wrapper","mat-mdc-form-field-bottom-align"],[1,"mat-mdc-form-field-error-wrapper"],[1,"mat-mdc-form-field-hint-wrapper"],["matFormFieldFloatingLabel","",3,"floating","monitorResize","id"],["aria-hidden","true",1,"mat-mdc-form-field-required-marker","mdc-floating-label--required"],[3,"id"],[1,"mat-mdc-form-field-hint-spacer"]],template:function(i,o){if(i&1){let n=rA();OA(DT),x(0,yT,1,1,"ng-template",null,0,da),d(2,"div",6,1),G("click",function(r){return Y(n),J(o._control.onContainerClick(r))}),x(4,MT,1,0,"div",7),d(5,"div",8),x(6,bT,2,2,"div",9)(7,FT,3,0,"div",10)(8,vT,3,0,"div",11),d(9,"div",12),x(10,NT,1,1,null,13),IA(11),h(),x(12,GT,3,0,"div",14)(13,LT,3,0,"div",15),h(),x(14,_T,1,0,"div",16),h(),d(15,"div",17),x(16,KT,2,1,"div",18)(17,xT,5,2,"div",19),h()}if(i&2){let n;D(2),nA("mdc-text-field--filled",!o._hasOutline())("mdc-text-field--outlined",o._hasOutline())("mdc-text-field--no-label",!o._hasFloatingLabel())("mdc-text-field--disabled",o._control.disabled)("mdc-text-field--invalid",o._control.errorState),D(2),_(!o._hasOutline()&&!o._control.disabled?4:-1),D(2),_(o._hasOutline()?6:-1),D(),_(o._hasIconPrefix?7:-1),D(),_(o._hasTextPrefix?8:-1),D(2),_(!o._hasOutline()||o._forceDisplayInfixLabel()?10:-1),D(2),_(o._hasTextSuffix?12:-1),D(),_(o._hasIconSuffix?13:-1),D(),_(o._hasOutline()?-1:14),D(),nA("mat-mdc-form-field-subscript-dynamic-size",o.subscriptSizing==="dynamic"),D(),_((n=o._getDisplayedMessages())==="error"?16:n==="hint"?17:-1)}},dependencies:[Gk,Kk,Da,_k,Nk],styles:['.mdc-text-field{display:inline-flex;align-items:baseline;padding:0 16px;position:relative;box-sizing:border-box;overflow:hidden;will-change:opacity,transform,color;border-top-left-radius:4px;border-top-right-radius:4px;border-bottom-right-radius:0;border-bottom-left-radius:0}.mdc-text-field__input{width:100%;min-width:0;border:none;border-radius:0;background:none;padding:0;-moz-appearance:none;-webkit-appearance:none;height:28px}.mdc-text-field__input::-webkit-calendar-picker-indicator{display:none}.mdc-text-field__input::-ms-clear{display:none}.mdc-text-field__input:focus{outline:none}.mdc-text-field__input:invalid{box-shadow:none}.mdc-text-field__input::placeholder{opacity:0}.mdc-text-field__input::-moz-placeholder{opacity:0}.mdc-text-field__input::-webkit-input-placeholder{opacity:0}.mdc-text-field__input:-ms-input-placeholder{opacity:0}.mdc-text-field--no-label .mdc-text-field__input::placeholder,.mdc-text-field--focused .mdc-text-field__input::placeholder{opacity:1}.mdc-text-field--no-label .mdc-text-field__input::-moz-placeholder,.mdc-text-field--focused .mdc-text-field__input::-moz-placeholder{opacity:1}.mdc-text-field--no-label .mdc-text-field__input::-webkit-input-placeholder,.mdc-text-field--focused .mdc-text-field__input::-webkit-input-placeholder{opacity:1}.mdc-text-field--no-label .mdc-text-field__input:-ms-input-placeholder,.mdc-text-field--focused .mdc-text-field__input:-ms-input-placeholder{opacity:1}.mdc-text-field--disabled:not(.mdc-text-field--no-label) .mdc-text-field__input.mat-mdc-input-disabled-interactive::placeholder{opacity:0}.mdc-text-field--disabled:not(.mdc-text-field--no-label) .mdc-text-field__input.mat-mdc-input-disabled-interactive::-moz-placeholder{opacity:0}.mdc-text-field--disabled:not(.mdc-text-field--no-label) .mdc-text-field__input.mat-mdc-input-disabled-interactive::-webkit-input-placeholder{opacity:0}.mdc-text-field--disabled:not(.mdc-text-field--no-label) .mdc-text-field__input.mat-mdc-input-disabled-interactive:-ms-input-placeholder{opacity:0}.mdc-text-field--outlined .mdc-text-field__input,.mdc-text-field--filled.mdc-text-field--no-label .mdc-text-field__input{height:100%}.mdc-text-field--outlined .mdc-text-field__input{display:flex;border:none !important;background-color:rgba(0,0,0,0)}.mdc-text-field--disabled .mdc-text-field__input{pointer-events:auto}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-text-field__input{color:var(--mdc-filled-text-field-input-text-color, var(--mat-sys-on-surface));caret-color:var(--mdc-filled-text-field-caret-color, var(--mat-sys-primary))}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-text-field__input::placeholder{color:var(--mdc-filled-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-text-field__input::-moz-placeholder{color:var(--mdc-filled-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-text-field__input::-webkit-input-placeholder{color:var(--mdc-filled-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-text-field__input:-ms-input-placeholder{color:var(--mdc-filled-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled.mdc-text-field--invalid:not(.mdc-text-field--disabled) .mdc-text-field__input{caret-color:var(--mdc-filled-text-field-error-caret-color)}.mdc-text-field--filled.mdc-text-field--disabled .mdc-text-field__input{color:var(--mdc-filled-text-field-disabled-input-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mdc-text-field__input{color:var(--mdc-outlined-text-field-input-text-color, var(--mat-sys-on-surface));caret-color:var(--mdc-outlined-text-field-caret-color, var(--mat-sys-primary))}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mdc-text-field__input::placeholder{color:var(--mdc-outlined-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mdc-text-field__input::-moz-placeholder{color:var(--mdc-outlined-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mdc-text-field__input::-webkit-input-placeholder{color:var(--mdc-outlined-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mdc-text-field__input:-ms-input-placeholder{color:var(--mdc-outlined-text-field-input-text-placeholder-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--outlined.mdc-text-field--invalid:not(.mdc-text-field--disabled) .mdc-text-field__input{caret-color:var(--mdc-outlined-text-field-error-caret-color)}.mdc-text-field--outlined.mdc-text-field--disabled .mdc-text-field__input{color:var(--mdc-outlined-text-field-disabled-input-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}@media(forced-colors: active){.mdc-text-field--disabled .mdc-text-field__input{background-color:Window}}.mdc-text-field--filled{height:56px;border-bottom-right-radius:0;border-bottom-left-radius:0;border-top-left-radius:var(--mdc-filled-text-field-container-shape, var(--mat-sys-corner-extra-small));border-top-right-radius:var(--mdc-filled-text-field-container-shape, var(--mat-sys-corner-extra-small))}.mdc-text-field--filled:not(.mdc-text-field--disabled){background-color:var(--mdc-filled-text-field-container-color, var(--mat-sys-surface-variant))}.mdc-text-field--filled.mdc-text-field--disabled{background-color:var(--mdc-filled-text-field-disabled-container-color, color-mix(in srgb, var(--mat-sys-on-surface) 4%, transparent))}.mdc-text-field--outlined{height:56px;overflow:visible;padding-right:max(16px,var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small)));padding-left:max(16px,var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small)) + 4px)}[dir=rtl] .mdc-text-field--outlined{padding-right:max(16px,var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small)) + 4px);padding-left:max(16px,var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small)))}.mdc-floating-label{position:absolute;left:0;transform-origin:left top;line-height:1.15rem;text-align:left;text-overflow:ellipsis;white-space:nowrap;cursor:text;overflow:hidden;will-change:transform}[dir=rtl] .mdc-floating-label{right:0;left:auto;transform-origin:right top;text-align:right}.mdc-text-field .mdc-floating-label{top:50%;transform:translateY(-50%);pointer-events:none}.mdc-notched-outline .mdc-floating-label{display:inline-block;position:relative;max-width:100%}.mdc-text-field--outlined .mdc-floating-label{left:4px;right:auto}[dir=rtl] .mdc-text-field--outlined .mdc-floating-label{left:auto;right:4px}.mdc-text-field--filled .mdc-floating-label{left:16px;right:auto}[dir=rtl] .mdc-text-field--filled .mdc-floating-label{left:auto;right:16px}.mdc-text-field--disabled .mdc-floating-label{cursor:default}@media(forced-colors: active){.mdc-text-field--disabled .mdc-floating-label{z-index:1}}.mdc-text-field--filled.mdc-text-field--no-label .mdc-floating-label{display:none}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-floating-label{color:var(--mdc-filled-text-field-label-text-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled:not(.mdc-text-field--disabled).mdc-text-field--focused .mdc-floating-label{color:var(--mdc-filled-text-field-focus-label-text-color, var(--mat-sys-primary))}.mdc-text-field--filled:not(.mdc-text-field--disabled):not(.mdc-text-field--focused):hover .mdc-floating-label{color:var(--mdc-filled-text-field-hover-label-text-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled.mdc-text-field--disabled .mdc-floating-label{color:var(--mdc-filled-text-field-disabled-label-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mdc-text-field--filled:not(.mdc-text-field--disabled).mdc-text-field--invalid .mdc-floating-label{color:var(--mdc-filled-text-field-error-label-text-color, var(--mat-sys-error))}.mdc-text-field--filled:not(.mdc-text-field--disabled).mdc-text-field--invalid.mdc-text-field--focused .mdc-floating-label{color:var(--mdc-filled-text-field-error-focus-label-text-color, var(--mat-sys-error))}.mdc-text-field--filled:not(.mdc-text-field--disabled).mdc-text-field--invalid:not(.mdc-text-field--disabled):hover .mdc-floating-label{color:var(--mdc-filled-text-field-error-hover-label-text-color, var(--mat-sys-on-error-container))}.mdc-text-field--filled .mdc-floating-label{font-family:var(--mdc-filled-text-field-label-text-font, var(--mat-sys-body-large-font));font-size:var(--mdc-filled-text-field-label-text-size, var(--mat-sys-body-large-size));font-weight:var(--mdc-filled-text-field-label-text-weight, var(--mat-sys-body-large-weight));letter-spacing:var(--mdc-filled-text-field-label-text-tracking, var(--mat-sys-body-large-tracking))}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mdc-floating-label{color:var(--mdc-outlined-text-field-label-text-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--focused .mdc-floating-label{color:var(--mdc-outlined-text-field-focus-label-text-color, var(--mat-sys-primary))}.mdc-text-field--outlined:not(.mdc-text-field--disabled):not(.mdc-text-field--focused):hover .mdc-floating-label{color:var(--mdc-outlined-text-field-hover-label-text-color, var(--mat-sys-on-surface))}.mdc-text-field--outlined.mdc-text-field--disabled .mdc-floating-label{color:var(--mdc-outlined-text-field-disabled-label-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--invalid .mdc-floating-label{color:var(--mdc-outlined-text-field-error-label-text-color, var(--mat-sys-error))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--invalid.mdc-text-field--focused .mdc-floating-label{color:var(--mdc-outlined-text-field-error-focus-label-text-color, var(--mat-sys-error))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--invalid:not(.mdc-text-field--disabled):hover .mdc-floating-label{color:var(--mdc-outlined-text-field-error-hover-label-text-color, var(--mat-sys-on-error-container))}.mdc-text-field--outlined .mdc-floating-label{font-family:var(--mdc-outlined-text-field-label-text-font, var(--mat-sys-body-large-font));font-size:var(--mdc-outlined-text-field-label-text-size, var(--mat-sys-body-large-size));font-weight:var(--mdc-outlined-text-field-label-text-weight, var(--mat-sys-body-large-weight));letter-spacing:var(--mdc-outlined-text-field-label-text-tracking, var(--mat-sys-body-large-tracking))}.mdc-floating-label--float-above{cursor:auto;transform:translateY(-106%) scale(0.75)}.mdc-text-field--filled .mdc-floating-label--float-above{transform:translateY(-106%) scale(0.75)}.mdc-text-field--outlined .mdc-floating-label--float-above{transform:translateY(-37.25px) scale(1);font-size:.75rem}.mdc-notched-outline .mdc-floating-label--float-above{text-overflow:clip}.mdc-notched-outline--upgraded .mdc-floating-label--float-above{max-width:133.3333333333%}.mdc-text-field--outlined.mdc-notched-outline--upgraded .mdc-floating-label--float-above,.mdc-text-field--outlined .mdc-notched-outline--upgraded .mdc-floating-label--float-above{transform:translateY(-34.75px) scale(0.75)}.mdc-text-field--outlined.mdc-notched-outline--upgraded .mdc-floating-label--float-above,.mdc-text-field--outlined .mdc-notched-outline--upgraded .mdc-floating-label--float-above{font-size:1rem}.mdc-floating-label--required:not(.mdc-floating-label--hide-required-marker)::after{margin-left:1px;margin-right:0;content:"*"}[dir=rtl] .mdc-floating-label--required:not(.mdc-floating-label--hide-required-marker)::after{margin-left:0;margin-right:1px}.mdc-notched-outline{display:flex;position:absolute;top:0;right:0;left:0;box-sizing:border-box;width:100%;max-width:100%;height:100%;text-align:left;pointer-events:none}[dir=rtl] .mdc-notched-outline{text-align:right}.mdc-text-field--outlined .mdc-notched-outline{z-index:1}.mat-mdc-notch-piece{box-sizing:border-box;height:100%;pointer-events:none;border-top:1px solid;border-bottom:1px solid}.mdc-text-field--focused .mat-mdc-notch-piece{border-width:2px}.mdc-text-field--outlined:not(.mdc-text-field--disabled) .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-outline-color, var(--mat-sys-outline));border-width:var(--mdc-outlined-text-field-outline-width, 1px)}.mdc-text-field--outlined:not(.mdc-text-field--disabled):not(.mdc-text-field--focused):hover .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-hover-outline-color, var(--mat-sys-on-surface))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--focused .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-focus-outline-color, var(--mat-sys-primary))}.mdc-text-field--outlined.mdc-text-field--disabled .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-disabled-outline-color, color-mix(in srgb, var(--mat-sys-on-surface) 12%, transparent))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--invalid .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-error-outline-color, var(--mat-sys-error))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--invalid:not(.mdc-text-field--focused):hover .mdc-notched-outline .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-error-hover-outline-color, var(--mat-sys-on-error-container))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--invalid.mdc-text-field--focused .mat-mdc-notch-piece{border-color:var(--mdc-outlined-text-field-error-focus-outline-color, var(--mat-sys-error))}.mdc-text-field--outlined:not(.mdc-text-field--disabled).mdc-text-field--focused .mdc-notched-outline .mat-mdc-notch-piece{border-width:var(--mdc-outlined-text-field-focus-outline-width, 2px)}.mdc-notched-outline__leading{border-left:1px solid;border-right:none;border-top-right-radius:0;border-bottom-right-radius:0;border-top-left-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small));border-bottom-left-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small))}.mdc-text-field--outlined .mdc-notched-outline .mdc-notched-outline__leading{width:max(12px,var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small)))}[dir=rtl] .mdc-notched-outline__leading{border-left:none;border-right:1px solid;border-bottom-left-radius:0;border-top-left-radius:0;border-top-right-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small));border-bottom-right-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small))}.mdc-notched-outline__trailing{flex-grow:1;border-left:none;border-right:1px solid;border-top-left-radius:0;border-bottom-left-radius:0;border-top-right-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small));border-bottom-right-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small))}[dir=rtl] .mdc-notched-outline__trailing{border-left:1px solid;border-right:none;border-top-right-radius:0;border-bottom-right-radius:0;border-top-left-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small));border-bottom-left-radius:var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small))}.mdc-notched-outline__notch{flex:0 0 auto;width:auto}.mdc-text-field--outlined .mdc-notched-outline .mdc-notched-outline__notch{max-width:min(var(--mat-form-field-notch-max-width, 100%),100% - max(12px,var(--mdc-outlined-text-field-container-shape, var(--mat-sys-corner-extra-small)))*2)}.mdc-text-field--outlined .mdc-notched-outline--notched .mdc-notched-outline__notch{padding-top:1px}.mdc-text-field--focused.mdc-text-field--outlined .mdc-notched-outline--notched .mdc-notched-outline__notch{padding-top:2px}.mdc-notched-outline--notched .mdc-notched-outline__notch{padding-left:0;padding-right:8px;border-top:none;--mat-form-field-notch-max-width: 100%}[dir=rtl] .mdc-notched-outline--notched .mdc-notched-outline__notch{padding-left:8px;padding-right:0}.mdc-notched-outline--no-label .mdc-notched-outline__notch{display:none}.mdc-line-ripple::before,.mdc-line-ripple::after{position:absolute;bottom:0;left:0;width:100%;border-bottom-style:solid;content:""}.mdc-line-ripple::before{z-index:1;border-bottom-width:var(--mdc-filled-text-field-active-indicator-height, 1px)}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-line-ripple::before{border-bottom-color:var(--mdc-filled-text-field-active-indicator-color, var(--mat-sys-on-surface-variant))}.mdc-text-field--filled:not(.mdc-text-field--disabled):not(.mdc-text-field--focused):hover .mdc-line-ripple::before{border-bottom-color:var(--mdc-filled-text-field-hover-active-indicator-color, var(--mat-sys-on-surface))}.mdc-text-field--filled.mdc-text-field--disabled .mdc-line-ripple::before{border-bottom-color:var(--mdc-filled-text-field-disabled-active-indicator-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mdc-text-field--filled:not(.mdc-text-field--disabled).mdc-text-field--invalid .mdc-line-ripple::before{border-bottom-color:var(--mdc-filled-text-field-error-active-indicator-color, var(--mat-sys-error))}.mdc-text-field--filled:not(.mdc-text-field--disabled).mdc-text-field--invalid:not(.mdc-text-field--focused):hover .mdc-line-ripple::before{border-bottom-color:var(--mdc-filled-text-field-error-hover-active-indicator-color, var(--mat-sys-on-error-container))}.mdc-line-ripple::after{transform:scaleX(0);opacity:0;z-index:2}.mdc-text-field--filled .mdc-line-ripple::after{border-bottom-width:var(--mdc-filled-text-field-focus-active-indicator-height, 2px)}.mdc-text-field--filled:not(.mdc-text-field--disabled) .mdc-line-ripple::after{border-bottom-color:var(--mdc-filled-text-field-focus-active-indicator-color, var(--mat-sys-primary))}.mdc-text-field--filled.mdc-text-field--invalid:not(.mdc-text-field--disabled) .mdc-line-ripple::after{border-bottom-color:var(--mdc-filled-text-field-error-focus-active-indicator-color, var(--mat-sys-error))}.mdc-line-ripple--active::after{transform:scaleX(1);opacity:1}.mdc-line-ripple--deactivating::after{opacity:0}.mdc-text-field--disabled{pointer-events:none}.mat-mdc-form-field-textarea-control{vertical-align:middle;resize:vertical;box-sizing:border-box;height:auto;margin:0;padding:0;border:none;overflow:auto}.mat-mdc-form-field-input-control.mat-mdc-form-field-input-control{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font:inherit;letter-spacing:inherit;text-decoration:inherit;text-transform:inherit;border:none}.mat-mdc-form-field .mat-mdc-floating-label.mdc-floating-label{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;line-height:normal;pointer-events:all;will-change:auto}.mat-mdc-form-field:not(.mat-form-field-disabled) .mat-mdc-floating-label.mdc-floating-label{cursor:inherit}.mdc-text-field--no-label:not(.mdc-text-field--textarea) .mat-mdc-form-field-input-control.mdc-text-field__input,.mat-mdc-text-field-wrapper .mat-mdc-form-field-input-control{height:auto}.mat-mdc-text-field-wrapper .mat-mdc-form-field-input-control.mdc-text-field__input[type=color]{height:23px}.mat-mdc-text-field-wrapper{height:auto;flex:auto;will-change:auto}.mat-mdc-form-field-has-icon-prefix .mat-mdc-text-field-wrapper{padding-left:0;--mat-mdc-form-field-label-offset-x: -16px}.mat-mdc-form-field-has-icon-suffix .mat-mdc-text-field-wrapper{padding-right:0}[dir=rtl] .mat-mdc-text-field-wrapper{padding-left:16px;padding-right:16px}[dir=rtl] .mat-mdc-form-field-has-icon-suffix .mat-mdc-text-field-wrapper{padding-left:0}[dir=rtl] .mat-mdc-form-field-has-icon-prefix .mat-mdc-text-field-wrapper{padding-right:0}.mat-form-field-disabled .mdc-text-field__input::placeholder{color:var(--mat-form-field-disabled-input-text-placeholder-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-form-field-disabled .mdc-text-field__input::-moz-placeholder{color:var(--mat-form-field-disabled-input-text-placeholder-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-form-field-disabled .mdc-text-field__input::-webkit-input-placeholder{color:var(--mat-form-field-disabled-input-text-placeholder-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-form-field-disabled .mdc-text-field__input:-ms-input-placeholder{color:var(--mat-form-field-disabled-input-text-placeholder-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-mdc-form-field-label-always-float .mdc-text-field__input::placeholder{transition-delay:40ms;transition-duration:110ms;opacity:1}.mat-mdc-text-field-wrapper .mat-mdc-form-field-infix .mat-mdc-floating-label{left:auto;right:auto}.mat-mdc-text-field-wrapper.mdc-text-field--outlined .mdc-text-field__input{display:inline-block}.mat-mdc-form-field .mat-mdc-text-field-wrapper.mdc-text-field .mdc-notched-outline__notch{padding-top:0}.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field .mdc-notched-outline__notch{border-left:1px solid rgba(0,0,0,0)}[dir=rtl] .mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field.mat-mdc-form-field .mdc-notched-outline__notch{border-left:none;border-right:1px solid rgba(0,0,0,0)}.mat-mdc-form-field-infix{min-height:var(--mat-form-field-container-height, 56px);padding-top:var(--mat-form-field-filled-with-label-container-padding-top, 24px);padding-bottom:var(--mat-form-field-filled-with-label-container-padding-bottom, 8px)}.mdc-text-field--outlined .mat-mdc-form-field-infix,.mdc-text-field--no-label .mat-mdc-form-field-infix{padding-top:var(--mat-form-field-container-vertical-padding, 16px);padding-bottom:var(--mat-form-field-container-vertical-padding, 16px)}.mat-mdc-text-field-wrapper .mat-mdc-form-field-flex .mat-mdc-floating-label{top:calc(var(--mat-form-field-container-height, 56px)/2)}.mdc-text-field--filled .mat-mdc-floating-label{display:var(--mat-form-field-filled-label-display, block)}.mat-mdc-text-field-wrapper.mdc-text-field--outlined .mdc-notched-outline--upgraded .mdc-floating-label--float-above{--mat-mdc-form-field-label-transform: translateY(calc(calc(6.75px + var(--mat-form-field-container-height, 56px) / 2) * -1)) scale(var(--mat-mdc-form-field-floating-label-scale, 0.75));transform:var(--mat-mdc-form-field-label-transform)}.mat-mdc-form-field-subscript-wrapper{box-sizing:border-box;width:100%;position:relative}.mat-mdc-form-field-hint-wrapper,.mat-mdc-form-field-error-wrapper{position:absolute;top:0;left:0;right:0;padding:0 16px}.mat-mdc-form-field-subscript-dynamic-size .mat-mdc-form-field-hint-wrapper,.mat-mdc-form-field-subscript-dynamic-size .mat-mdc-form-field-error-wrapper{position:static}.mat-mdc-form-field-bottom-align::before{content:"";display:inline-block;height:16px}.mat-mdc-form-field-bottom-align.mat-mdc-form-field-subscript-dynamic-size::before{content:unset}.mat-mdc-form-field-hint-end{order:1}.mat-mdc-form-field-hint-wrapper{display:flex}.mat-mdc-form-field-hint-spacer{flex:1 0 1em}.mat-mdc-form-field-error{display:block;color:var(--mat-form-field-error-text-color, var(--mat-sys-error))}.mat-mdc-form-field-subscript-wrapper,.mat-mdc-form-field-bottom-align::before{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:var(--mat-form-field-subscript-text-font, var(--mat-sys-body-small-font));line-height:var(--mat-form-field-subscript-text-line-height, var(--mat-sys-body-small-line-height));font-size:var(--mat-form-field-subscript-text-size, var(--mat-sys-body-small-size));letter-spacing:var(--mat-form-field-subscript-text-tracking, var(--mat-sys-body-small-tracking));font-weight:var(--mat-form-field-subscript-text-weight, var(--mat-sys-body-small-weight))}.mat-mdc-form-field-focus-overlay{top:0;left:0;right:0;bottom:0;position:absolute;opacity:0;pointer-events:none;background-color:var(--mat-form-field-state-layer-color, var(--mat-sys-on-surface))}.mat-mdc-text-field-wrapper:hover .mat-mdc-form-field-focus-overlay{opacity:var(--mat-form-field-hover-state-layer-opacity, var(--mat-sys-hover-state-layer-opacity))}.mat-mdc-form-field.mat-focused .mat-mdc-form-field-focus-overlay{opacity:var(--mat-form-field-focus-state-layer-opacity, 0)}select.mat-mdc-form-field-input-control{-moz-appearance:none;-webkit-appearance:none;background-color:rgba(0,0,0,0);display:inline-flex;box-sizing:border-box}select.mat-mdc-form-field-input-control:not(:disabled){cursor:pointer}select.mat-mdc-form-field-input-control:not(.mat-mdc-native-select-inline) option{color:var(--mat-form-field-select-option-text-color, var(--mat-sys-neutral10))}select.mat-mdc-form-field-input-control:not(.mat-mdc-native-select-inline) option:disabled{color:var(--mat-form-field-select-disabled-option-text-color, color-mix(in srgb, var(--mat-sys-neutral10) 38%, transparent))}.mat-mdc-form-field-type-mat-native-select .mat-mdc-form-field-infix::after{content:"";width:0;height:0;border-left:5px solid rgba(0,0,0,0);border-right:5px solid rgba(0,0,0,0);border-top:5px solid;position:absolute;right:0;top:50%;margin-top:-2.5px;pointer-events:none;color:var(--mat-form-field-enabled-select-arrow-color, var(--mat-sys-on-surface-variant))}[dir=rtl] .mat-mdc-form-field-type-mat-native-select .mat-mdc-form-field-infix::after{right:auto;left:0}.mat-mdc-form-field-type-mat-native-select.mat-focused .mat-mdc-form-field-infix::after{color:var(--mat-form-field-focus-select-arrow-color, var(--mat-sys-primary))}.mat-mdc-form-field-type-mat-native-select.mat-form-field-disabled .mat-mdc-form-field-infix::after{color:var(--mat-form-field-disabled-select-arrow-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-mdc-form-field-type-mat-native-select .mat-mdc-form-field-input-control{padding-right:15px}[dir=rtl] .mat-mdc-form-field-type-mat-native-select .mat-mdc-form-field-input-control{padding-right:0;padding-left:15px}@media(forced-colors: active){.mat-form-field-appearance-fill .mat-mdc-text-field-wrapper{outline:solid 1px}}@media(forced-colors: active){.mat-form-field-appearance-fill.mat-form-field-disabled .mat-mdc-text-field-wrapper{outline-color:GrayText}}@media(forced-colors: active){.mat-form-field-appearance-fill.mat-focused .mat-mdc-text-field-wrapper{outline:dashed 3px}}@media(forced-colors: active){.mat-mdc-form-field.mat-focused .mdc-notched-outline{border:dashed 3px}}.mat-mdc-form-field-input-control[type=date],.mat-mdc-form-field-input-control[type=datetime],.mat-mdc-form-field-input-control[type=datetime-local],.mat-mdc-form-field-input-control[type=month],.mat-mdc-form-field-input-control[type=week],.mat-mdc-form-field-input-control[type=time]{line-height:1}.mat-mdc-form-field-input-control::-webkit-datetime-edit{line-height:1;padding:0;margin-bottom:-2px}.mat-mdc-form-field{--mat-mdc-form-field-floating-label-scale: 0.75;display:inline-flex;flex-direction:column;min-width:0;text-align:left;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:var(--mat-form-field-container-text-font, var(--mat-sys-body-large-font));line-height:var(--mat-form-field-container-text-line-height, var(--mat-sys-body-large-line-height));font-size:var(--mat-form-field-container-text-size, var(--mat-sys-body-large-size));letter-spacing:var(--mat-form-field-container-text-tracking, var(--mat-sys-body-large-tracking));font-weight:var(--mat-form-field-container-text-weight, var(--mat-sys-body-large-weight))}.mat-mdc-form-field .mdc-text-field--outlined .mdc-floating-label--float-above{font-size:calc(var(--mat-form-field-outlined-label-text-populated-size)*var(--mat-mdc-form-field-floating-label-scale))}.mat-mdc-form-field .mdc-text-field--outlined .mdc-notched-outline--upgraded .mdc-floating-label--float-above{font-size:var(--mat-form-field-outlined-label-text-populated-size)}[dir=rtl] .mat-mdc-form-field{text-align:right}.mat-mdc-form-field-flex{display:inline-flex;align-items:baseline;box-sizing:border-box;width:100%}.mat-mdc-text-field-wrapper{width:100%;z-index:0}.mat-mdc-form-field-icon-prefix,.mat-mdc-form-field-icon-suffix{align-self:center;line-height:0;pointer-events:auto;position:relative;z-index:1}.mat-mdc-form-field-icon-prefix>.mat-icon,.mat-mdc-form-field-icon-suffix>.mat-icon{padding:0 12px;box-sizing:content-box}.mat-mdc-form-field-icon-prefix{color:var(--mat-form-field-leading-icon-color, var(--mat-sys-on-surface-variant))}.mat-form-field-disabled .mat-mdc-form-field-icon-prefix{color:var(--mat-form-field-disabled-leading-icon-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-mdc-form-field-icon-suffix{color:var(--mat-form-field-trailing-icon-color, var(--mat-sys-on-surface-variant))}.mat-form-field-disabled .mat-mdc-form-field-icon-suffix{color:var(--mat-form-field-disabled-trailing-icon-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-form-field-invalid .mat-mdc-form-field-icon-suffix{color:var(--mat-form-field-error-trailing-icon-color, var(--mat-sys-error))}.mat-form-field-invalid:not(.mat-focused):not(.mat-form-field-disabled) .mat-mdc-text-field-wrapper:hover .mat-mdc-form-field-icon-suffix{color:var(--mat-form-field-error-hover-trailing-icon-color, var(--mat-sys-on-error-container))}.mat-form-field-invalid.mat-focused .mat-mdc-text-field-wrapper .mat-mdc-form-field-icon-suffix{color:var(--mat-form-field-error-focus-trailing-icon-color, var(--mat-sys-error))}.mat-mdc-form-field-icon-prefix,[dir=rtl] .mat-mdc-form-field-icon-suffix{padding:0 4px 0 0}.mat-mdc-form-field-icon-suffix,[dir=rtl] .mat-mdc-form-field-icon-prefix{padding:0 0 0 4px}.mat-mdc-form-field-subscript-wrapper .mat-icon,.mat-mdc-form-field label .mat-icon{width:1em;height:1em;font-size:inherit}.mat-mdc-form-field-infix{flex:auto;min-width:0;width:180px;position:relative;box-sizing:border-box}.mat-mdc-form-field-infix:has(textarea[cols]){width:auto}.mat-mdc-form-field .mdc-notched-outline__notch{margin-left:-1px;-webkit-clip-path:inset(-9em -999em -9em 1px);clip-path:inset(-9em -999em -9em 1px)}[dir=rtl] .mat-mdc-form-field .mdc-notched-outline__notch{margin-left:0;margin-right:-1px;-webkit-clip-path:inset(-9em 1px -9em -999em);clip-path:inset(-9em 1px -9em -999em)}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-floating-label{transition:transform 150ms cubic-bezier(0.4, 0, 0.2, 1),color 150ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-text-field__input{transition:opacity 150ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-text-field__input::placeholder{transition:opacity 67ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-text-field__input::-moz-placeholder{transition:opacity 67ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-text-field__input::-webkit-input-placeholder{transition:opacity 67ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-text-field__input:-ms-input-placeholder{transition:opacity 67ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--no-label .mdc-text-field__input::placeholder,.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--focused .mdc-text-field__input::placeholder{transition-delay:40ms;transition-duration:110ms}.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--no-label .mdc-text-field__input::-moz-placeholder,.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--focused .mdc-text-field__input::-moz-placeholder{transition-delay:40ms;transition-duration:110ms}.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--no-label .mdc-text-field__input::-webkit-input-placeholder,.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--focused .mdc-text-field__input::-webkit-input-placeholder{transition-delay:40ms;transition-duration:110ms}.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--no-label .mdc-text-field__input:-ms-input-placeholder,.mat-mdc-form-field:not(.mat-form-field-no-animations).mdc-text-field--focused .mdc-text-field__input:-ms-input-placeholder{transition-delay:40ms;transition-duration:110ms}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-text-field--filled:not(.mdc-ripple-upgraded):focus .mdc-text-field__ripple::before{transition-duration:75ms}.mat-mdc-form-field:not(.mat-form-field-no-animations) .mdc-line-ripple::after{transition:transform 180ms cubic-bezier(0.4, 0, 0.2, 1),opacity 180ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-notched-outline .mdc-floating-label{max-width:calc(100% + 1px)}.mdc-notched-outline--upgraded .mdc-floating-label--float-above{max-width:calc(133.3333333333% + 1px)}'],encapsulation:2,data:{animation:[TT.transitionMessages]},changeDetection:0})}return t})(),tn=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({imports:[mA,ts,mA]})}return t})();var qT=["trigger"],VT=["panel"],WT=[[["mat-select-trigger"]],"*"],zT=["mat-select-trigger","*"];function jT(t,e){if(t&1&&(d(0,"span",4),k(1),h()),t&2){let A=y();D(),NA(A.placeholder)}}function XT(t,e){t&1&&IA(0)}function $T(t,e){if(t&1&&(d(0,"span",11),k(1),h()),t&2){let A=y(2);D(),NA(A.triggerValue)}}function A2(t,e){if(t&1&&(d(0,"span",5),x(1,XT,1,0)(2,$T,2,1,"span",11),h()),t&2){let A=y();D(),_(A.customTrigger?1:2)}}function e2(t,e){if(t&1){let A=rA();d(0,"div",12,1),G("@transformPanel.done",function(o){Y(A);let n=y();return J(n._panelDoneAnimatingStream.next(o.toState))})("keydown",function(o){Y(A);let n=y();return J(n._handleKeydown(o))}),IA(2,1),h()}if(t&2){let A=y();f0("mat-mdc-select-panel mdc-menu-surface mdc-menu-surface--open ",A._getPanelTheme(),""),L("ngClass",A.panelClass)("@transformPanel","showing"),aA("id",A.id+"-panel")("aria-multiselectable",A.multiple)("aria-label",A.ariaLabel||null)("aria-labelledby",A._getPanelAriaLabelledby())}}var t2={transformPanelWrap:lo("transformPanelWrap",[xt("* => void",Gm("@transformPanel",[Nm()],{optional:!0}))]),transformPanel:lo("transformPanel",[li("void",Ue({opacity:0,transform:"scale(1, 0.8)"})),xt("void => showing",ti("120ms cubic-bezier(0, 0, 0.2, 1)",Ue({opacity:1,transform:"scale(1, 1)"}))),xt("* => void",ti("100ms linear",Ue({opacity:0})))])};var Tk=new F("mat-select-scroll-strategy",{providedIn:"root",factory:()=>{let t=B(je);return()=>t.scrollStrategies.reposition()}});function i2(t){return()=>t.scrollStrategies.reposition()}var o2=new F("MAT_SELECT_CONFIG"),n2={provide:Tk,deps:[je],useFactory:i2},g2=new F("MatSelectTrigger"),Lm=class{source;value;constructor(e,A){this.source=e,this.value=A}},Cs=(()=>{class t{_viewportRuler=B(Bi);_changeDetectorRef=B(KA);_elementRef=B(q);_dir=B(Se,{optional:!0});_idGenerator=B(re);_parentFormField=B(hI,{optional:!0});ngControl=B(Ni,{self:!0,optional:!0});_liveAnnouncer=B(DE);_defaultOptions=B(o2,{optional:!0});_initialized=new U;options;optionGroups;customTrigger;_positions=[{originX:"start",originY:"bottom",overlayX:"start",overlayY:"top"},{originX:"end",originY:"bottom",overlayX:"end",overlayY:"top"},{originX:"start",originY:"top",overlayX:"start",overlayY:"bottom",panelClass:"mat-mdc-select-panel-above"},{originX:"end",originY:"top",overlayX:"end",overlayY:"bottom",panelClass:"mat-mdc-select-panel-above"}];_scrollOptionIntoView(A){let i=this.options.toArray()[A];if(i){let o=this.panel.nativeElement,n=Ek(A,this.options,this.optionGroups),g=i._getHostElement();A===0&&n===1?o.scrollTop=0:o.scrollTop=ck(g.offsetTop,g.offsetHeight,o.scrollTop,o.offsetHeight)}}_positioningSettled(){this._scrollOptionIntoView(this._keyManager.activeItemIndex||0)}_getChangeEvent(A){return new Lm(this,A)}_scrollStrategyFactory=B(Tk);_panelOpen=!1;_compareWith=(A,i)=>A===i;_uid=this._idGenerator.getId("mat-select-");_triggerAriaLabelledBy=null;_previousControl;_destroy=new U;_errorStateTracker;stateChanges=new U;disableAutomaticLabeling=!0;userAriaDescribedBy;_selectionModel;_keyManager;_preferredOverlayOrigin;_overlayWidth;_onChange=()=>{};_onTouched=()=>{};_valueId=this._idGenerator.getId("mat-select-value-");_panelDoneAnimatingStream=new U;_scrollStrategy;_overlayPanelClass=this._defaultOptions?.overlayPanelClass||"";get focused(){return this._focused||this._panelOpen}_focused=!1;controlType="mat-select";trigger;panel;_overlayDir;panelClass;disabled=!1;disableRipple=!1;tabIndex=0;get hideSingleSelectionIndicator(){return this._hideSingleSelectionIndicator}set hideSingleSelectionIndicator(A){this._hideSingleSelectionIndicator=A,this._syncParentProperties()}_hideSingleSelectionIndicator=this._defaultOptions?.hideSingleSelectionIndicator??!1;get placeholder(){return this._placeholder}set placeholder(A){this._placeholder=A,this.stateChanges.next()}_placeholder;get required(){return this._required??this.ngControl?.control?.hasValidator(_r.required)??!1}set required(A){this._required=A,this.stateChanges.next()}_required;get multiple(){return this._multiple}set multiple(A){this._selectionModel,this._multiple=A}_multiple=!1;disableOptionCentering=this._defaultOptions?.disableOptionCentering??!1;get compareWith(){return this._compareWith}set compareWith(A){this._compareWith=A,this._selectionModel&&this._initializeSelection()}get value(){return this._value}set value(A){this._assignValue(A)&&this._onChange(A)}_value;ariaLabel="";ariaLabelledby;get errorStateMatcher(){return this._errorStateTracker.matcher}set errorStateMatcher(A){this._errorStateTracker.matcher=A}typeaheadDebounceInterval;sortComparator;get id(){return this._id}set id(A){this._id=A||this._uid,this.stateChanges.next()}_id;get errorState(){return this._errorStateTracker.errorState}set errorState(A){this._errorStateTracker.errorState=A}panelWidth=this._defaultOptions&&typeof this._defaultOptions.panelWidth<"u"?this._defaultOptions.panelWidth:"auto";canSelectNullableOptions=this._defaultOptions?.canSelectNullableOptions??!1;optionSelectionChanges=Zi(()=>{let A=this.options;return A?A.changes.pipe(Me(A),Ie(()=>ye(...A.map(i=>i.onSelectionChange)))):this._initialized.pipe(Ie(()=>this.optionSelectionChanges))});openedChange=new z;_openedStream=this.openedChange.pipe(kA(A=>A),sA(()=>{}));_closedStream=this.openedChange.pipe(kA(A=>!A),sA(()=>{}));selectionChange=new z;valueChange=new z;constructor(){let A=B(ns),i=B(Ja,{optional:!0}),o=B(Ha,{optional:!0}),n=B(new Ct("tabindex"),{optional:!0});this.ngControl&&(this.ngControl.valueAccessor=this),this._defaultOptions?.typeaheadDebounceInterval!=null&&(this.typeaheadDebounceInterval=this._defaultOptions.typeaheadDebounceInterval),this._errorStateTracker=new Rg(A,this.ngControl,o,i,this.stateChanges),this._scrollStrategy=this._scrollStrategyFactory(),this.tabIndex=n==null?0:parseInt(n)||0,this.id=this.id}ngOnInit(){this._selectionModel=new Gn(this.multiple),this.stateChanges.next(),this._panelDoneAnimatingStream.pipe(wi(),pA(this._destroy)).subscribe(()=>this._panelDoneAnimating(this.panelOpen)),this._viewportRuler.change().pipe(pA(this._destroy)).subscribe(()=>{this.panelOpen&&(this._overlayWidth=this._getOverlayWidth(this._preferredOverlayOrigin),this._changeDetectorRef.detectChanges())})}ngAfterContentInit(){this._initialized.next(),this._initialized.complete(),this._initKeyManager(),this._selectionModel.changed.pipe(pA(this._destroy)).subscribe(A=>{A.added.forEach(i=>i.select()),A.removed.forEach(i=>i.deselect())}),this.options.changes.pipe(Me(null),pA(this._destroy)).subscribe(()=>{this._resetOptions(),this._initializeSelection()})}ngDoCheck(){let A=this._getTriggerAriaLabelledby(),i=this.ngControl;if(A!==this._triggerAriaLabelledBy){let o=this._elementRef.nativeElement;this._triggerAriaLabelledBy=A,A?o.setAttribute("aria-labelledby",A):o.removeAttribute("aria-labelledby")}i&&(this._previousControl!==i.control&&(this._previousControl!==void 0&&i.disabled!==null&&i.disabled!==this.disabled&&(this.disabled=i.disabled),this._previousControl=i.control),this.updateErrorState())}ngOnChanges(A){(A.disabled||A.userAriaDescribedBy)&&this.stateChanges.next(),A.typeaheadDebounceInterval&&this._keyManager&&this._keyManager.withTypeAhead(this.typeaheadDebounceInterval)}ngOnDestroy(){this._keyManager?.destroy(),this._destroy.next(),this._destroy.complete(),this.stateChanges.complete(),this._clearFromModal()}toggle(){this.panelOpen?this.close():this.open()}open(){this._canOpen()&&(this._parentFormField&&(this._preferredOverlayOrigin=this._parentFormField.getConnectedOverlayOrigin()),this._overlayWidth=this._getOverlayWidth(this._preferredOverlayOrigin),this._applyModalPanelOwnership(),this._panelOpen=!0,this._keyManager.withHorizontalOrientation(null),this._highlightCorrectOption(),this._changeDetectorRef.markForCheck(),this.stateChanges.next())}_trackedModal=null;_applyModalPanelOwnership(){let A=this._elementRef.nativeElement.closest('body > .cdk-overlay-container [aria-modal="true"]');if(!A)return;let i=`${this.id}-panel`;this._trackedModal&&uE(this._trackedModal,"aria-owns",i),om(A,"aria-owns",i),this._trackedModal=A}_clearFromModal(){if(!this._trackedModal)return;let A=`${this.id}-panel`;uE(this._trackedModal,"aria-owns",A),this._trackedModal=null}close(){this._panelOpen&&(this._panelOpen=!1,this._keyManager.withHorizontalOrientation(this._isRtl()?"rtl":"ltr"),this._changeDetectorRef.markForCheck(),this._onTouched(),this.stateChanges.next())}writeValue(A){this._assignValue(A)}registerOnChange(A){this._onChange=A}registerOnTouched(A){this._onTouched=A}setDisabledState(A){this.disabled=A,this._changeDetectorRef.markForCheck(),this.stateChanges.next()}get panelOpen(){return this._panelOpen}get selected(){return this.multiple?this._selectionModel?.selected||[]:this._selectionModel?.selected[0]}get triggerValue(){if(this.empty)return"";if(this._multiple){let A=this._selectionModel.selected.map(i=>i.viewValue);return this._isRtl()&&A.reverse(),A.join(", ")}return this._selectionModel.selected[0].viewValue}updateErrorState(){this._errorStateTracker.updateErrorState()}_isRtl(){return this._dir?this._dir.value==="rtl":!1}_handleKeydown(A){this.disabled||(this.panelOpen?this._handleOpenKeydown(A):this._handleClosedKeydown(A))}_handleClosedKeydown(A){let i=A.keyCode,o=i===40||i===38||i===37||i===39,n=i===13||i===32,g=this._keyManager;if(!g.isTyping()&&n&&!ze(A)||(this.multiple||A.altKey)&&o)A.preventDefault(),this.open();else if(!this.multiple){let r=this.selected;g.onKeydown(A);let s=this.selected;s&&r!==s&&this._liveAnnouncer.announce(s.viewValue,1e4)}}_handleOpenKeydown(A){let i=this._keyManager,o=A.keyCode,n=o===40||o===38,g=i.isTyping();if(n&&A.altKey)A.preventDefault(),this.close();else if(!g&&(o===13||o===32)&&i.activeItem&&!ze(A))A.preventDefault(),i.activeItem._selectViaInteraction();else if(!g&&this._multiple&&o===65&&A.ctrlKey){A.preventDefault();let r=this.options.some(s=>!s.disabled&&!s.selected);this.options.forEach(s=>{s.disabled||(r?s.select():s.deselect())})}else{let r=i.activeItemIndex;i.onKeydown(A),this._multiple&&n&&A.shiftKey&&i.activeItem&&i.activeItemIndex!==r&&i.activeItem._selectViaInteraction()}}_onFocus(){this.disabled||(this._focused=!0,this.stateChanges.next())}_onBlur(){this._focused=!1,this._keyManager?.cancelTypeahead(),!this.disabled&&!this.panelOpen&&(this._onTouched(),this._changeDetectorRef.markForCheck(),this.stateChanges.next())}_onAttached(){this._overlayDir.positionChange.pipe(ue(1)).subscribe(()=>{this._changeDetectorRef.detectChanges(),this._positioningSettled()})}_getPanelTheme(){return this._parentFormField?`mat-${this._parentFormField.color}`:""}get empty(){return!this._selectionModel||this._selectionModel.isEmpty()}_initializeSelection(){Promise.resolve().then(()=>{this.ngControl&&(this._value=this.ngControl.value),this._setSelectionByValue(this._value),this.stateChanges.next()})}_setSelectionByValue(A){if(this.options.forEach(i=>i.setInactiveStyles()),this._selectionModel.clear(),this.multiple&&A)Array.isArray(A),A.forEach(i=>this._selectOptionByValue(i)),this._sortValues();else{let i=this._selectOptionByValue(A);i?this._keyManager.updateActiveItem(i):this.panelOpen||this._keyManager.updateActiveItem(-1)}this._changeDetectorRef.markForCheck()}_selectOptionByValue(A){let i=this.options.find(o=>{if(this._selectionModel.isSelected(o))return!1;try{return(o.value!=null||this.canSelectNullableOptions)&&this._compareWith(o.value,A)}catch{return!1}});return i&&this._selectionModel.select(i),i}_assignValue(A){return A!==this._value||this._multiple&&Array.isArray(A)?(this.options&&this._setSelectionByValue(A),this._value=A,!0):!1}_skipPredicate=A=>this.panelOpen?!1:A.disabled;_getOverlayWidth(A){return this.panelWidth==="auto"?(A instanceof lI?A.elementRef:A||this._elementRef).nativeElement.getBoundingClientRect().width:this.panelWidth===null?"":this.panelWidth}_syncParentProperties(){if(this.options)for(let A of this.options)A._changeDetectorRef.markForCheck()}_initKeyManager(){this._keyManager=new cE(this.options).withTypeAhead(this.typeaheadDebounceInterval).withVerticalOrientation().withHorizontalOrientation(this._isRtl()?"rtl":"ltr").withHomeAndEnd().withPageUpDown().withAllowedModifierKeys(["shiftKey"]).skipPredicate(this._skipPredicate),this._keyManager.tabOut.subscribe(()=>{this.panelOpen&&(!this.multiple&&this._keyManager.activeItem&&this._keyManager.activeItem._selectViaInteraction(),this.focus(),this.close())}),this._keyManager.change.subscribe(()=>{this._panelOpen&&this.panel?this._scrollOptionIntoView(this._keyManager.activeItemIndex||0):!this._panelOpen&&!this.multiple&&this._keyManager.activeItem&&this._keyManager.activeItem._selectViaInteraction()})}_resetOptions(){let A=ye(this.options.changes,this._destroy);this.optionSelectionChanges.pipe(pA(A)).subscribe(i=>{this._onSelect(i.source,i.isUserInput),i.isUserInput&&!this.multiple&&this._panelOpen&&(this.close(),this.focus())}),ye(...this.options.map(i=>i._stateChanges)).pipe(pA(A)).subscribe(()=>{this._changeDetectorRef.detectChanges(),this.stateChanges.next()})}_onSelect(A,i){let o=this._selectionModel.isSelected(A);!this.canSelectNullableOptions&&A.value==null&&!this._multiple?(A.deselect(),this._selectionModel.clear(),this.value!=null&&this._propagateChanges(A.value)):(o!==A.selected&&(A.selected?this._selectionModel.select(A):this._selectionModel.deselect(A)),i&&this._keyManager.setActiveItem(A),this.multiple&&(this._sortValues(),i&&this.focus())),o!==this._selectionModel.isSelected(A)&&this._propagateChanges(),this.stateChanges.next()}_sortValues(){if(this.multiple){let A=this.options.toArray();this._selectionModel.sort((i,o)=>this.sortComparator?this.sortComparator(i,o,A):A.indexOf(i)-A.indexOf(o)),this.stateChanges.next()}}_propagateChanges(A){let i;this.multiple?i=this.selected.map(o=>o.value):i=this.selected?this.selected.value:A,this._value=i,this.valueChange.emit(i),this._onChange(i),this.selectionChange.emit(this._getChangeEvent(i)),this._changeDetectorRef.markForCheck()}_highlightCorrectOption(){if(this._keyManager)if(this.empty){let A=-1;for(let i=0;i<this.options.length;i++)if(!this.options.get(i).disabled){A=i;break}this._keyManager.setActiveItem(A)}else this._keyManager.setActiveItem(this._selectionModel.selected[0])}_canOpen(){return!this._panelOpen&&!this.disabled&&this.options?.length>0}focus(A){this._elementRef.nativeElement.focus(A)}_getPanelAriaLabelledby(){if(this.ariaLabel)return null;let A=this._parentFormField?.getLabelId()||null,i=A?A+" ":"";return this.ariaLabelledby?i+this.ariaLabelledby:A}_getAriaActiveDescendant(){return this.panelOpen&&this._keyManager&&this._keyManager.activeItem?this._keyManager.activeItem.id:null}_getTriggerAriaLabelledby(){if(this.ariaLabel)return null;let A=this._parentFormField?.getLabelId(),i=(A?A+" ":"")+this._valueId;return this.ariaLabelledby&&(i+=" "+this.ariaLabelledby),i}_panelDoneAnimating(A){this.openedChange.emit(A)}setDescribedByIds(A){A.length?this._elementRef.nativeElement.setAttribute("aria-describedby",A.join(" ")):this._elementRef.nativeElement.removeAttribute("aria-describedby")}onContainerClick(){this.focus(),this.open()}get shouldLabelFloat(){return this.panelOpen||!this.empty||this.focused&&!!this.placeholder}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["mat-select"]],contentQueries:function(i,o,n){if(i&1&&(XA(n,g2,5),XA(n,Nn,5),XA(n,dm,5)),i&2){let g;$(g=AA())&&(o.customTrigger=g.first),$(g=AA())&&(o.options=g),$(g=AA())&&(o.optionGroups=g)}},viewQuery:function(i,o){if(i&1&&(QA(qT,5),QA(VT,5),QA(vm,5)),i&2){let n;$(n=AA())&&(o.trigger=n.first),$(n=AA())&&(o.panel=n.first),$(n=AA())&&(o._overlayDir=n.first)}},hostAttrs:["role","combobox","aria-haspopup","listbox",1,"mat-mdc-select"],hostVars:19,hostBindings:function(i,o){i&1&&G("keydown",function(g){return o._handleKeydown(g)})("focus",function(){return o._onFocus()})("blur",function(){return o._onBlur()}),i&2&&(aA("id",o.id)("tabindex",o.disabled?-1:o.tabIndex)("aria-controls",o.panelOpen?o.id+"-panel":null)("aria-expanded",o.panelOpen)("aria-label",o.ariaLabel||null)("aria-required",o.required.toString())("aria-disabled",o.disabled.toString())("aria-invalid",o.errorState)("aria-activedescendant",o._getAriaActiveDescendant()),nA("mat-mdc-select-disabled",o.disabled)("mat-mdc-select-invalid",o.errorState)("mat-mdc-select-required",o.required)("mat-mdc-select-empty",o.empty)("mat-mdc-select-multiple",o.multiple))},inputs:{userAriaDescribedBy:[0,"aria-describedby","userAriaDescribedBy"],panelClass:"panelClass",disabled:[2,"disabled","disabled",eA],disableRipple:[2,"disableRipple","disableRipple",eA],tabIndex:[2,"tabIndex","tabIndex",A=>A==null?0:de(A)],hideSingleSelectionIndicator:[2,"hideSingleSelectionIndicator","hideSingleSelectionIndicator",eA],placeholder:"placeholder",required:[2,"required","required",eA],multiple:[2,"multiple","multiple",eA],disableOptionCentering:[2,"disableOptionCentering","disableOptionCentering",eA],compareWith:"compareWith",value:"value",ariaLabel:[0,"aria-label","ariaLabel"],ariaLabelledby:[0,"aria-labelledby","ariaLabelledby"],errorStateMatcher:"errorStateMatcher",typeaheadDebounceInterval:[2,"typeaheadDebounceInterval","typeaheadDebounceInterval",de],sortComparator:"sortComparator",id:"id",panelWidth:"panelWidth",canSelectNullableOptions:[2,"canSelectNullableOptions","canSelectNullableOptions",eA]},outputs:{openedChange:"openedChange",_openedStream:"opened",_closedStream:"closed",selectionChange:"selectionChange",valueChange:"valueChange"},exportAs:["matSelect"],features:[FA([{provide:dI,useExisting:t},{provide:lm,useExisting:t}]),TA],ngContentSelectors:zT,decls:11,vars:8,consts:[["fallbackOverlayOrigin","cdkOverlayOrigin","trigger",""],["panel",""],["cdk-overlay-origin","",1,"mat-mdc-select-trigger",3,"click"],[1,"mat-mdc-select-value"],[1,"mat-mdc-select-placeholder","mat-mdc-select-min-line"],[1,"mat-mdc-select-value-text"],[1,"mat-mdc-select-arrow-wrapper"],[1,"mat-mdc-select-arrow"],["viewBox","0 0 24 24","width","24px","height","24px","focusable","false","aria-hidden","true"],["d","M7 10l5 5 5-5z"],["cdk-connected-overlay","","cdkConnectedOverlayLockPosition","","cdkConnectedOverlayHasBackdrop","","cdkConnectedOverlayBackdropClass","cdk-overlay-transparent-backdrop",3,"backdropClick","attach","detach","cdkConnectedOverlayPanelClass","cdkConnectedOverlayScrollStrategy","cdkConnectedOverlayOrigin","cdkConnectedOverlayOpen","cdkConnectedOverlayPositions","cdkConnectedOverlayWidth"],[1,"mat-mdc-select-min-line"],["role","listbox","tabindex","-1",3,"keydown","ngClass"]],template:function(i,o){if(i&1){let n=rA();OA(WT),d(0,"div",2,0),G("click",function(){return Y(n),J(o.open())}),d(3,"div",3),x(4,jT,2,1,"span",4)(5,A2,3,1,"span",5),h(),d(6,"div",6)(7,"div",7),At(),d(8,"svg",8),P(9,"path",9),h()()()(),x(10,e2,3,9,"ng-template",10),G("backdropClick",function(){return Y(n),J(o.close())})("attach",function(){return Y(n),J(o._onAttached())})("detach",function(){return Y(n),J(o.close())})}if(i&2){let n=_e(1);D(3),aA("id",o._valueId),D(),_(o.empty?4:5),D(6),L("cdkConnectedOverlayPanelClass",o._overlayPanelClass)("cdkConnectedOverlayScrollStrategy",o._scrollStrategy)("cdkConnectedOverlayOrigin",o._preferredOverlayOrigin||n)("cdkConnectedOverlayOpen",o.panelOpen)("cdkConnectedOverlayPositions",o._positions)("cdkConnectedOverlayWidth",o._overlayWidth)}},dependencies:[lI,vm,zt],styles:['.mat-mdc-select{display:inline-block;width:100%;outline:none;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;color:var(--mat-select-enabled-trigger-text-color, var(--mat-sys-on-surface));font-family:var(--mat-select-trigger-text-font, var(--mat-sys-body-large-font));line-height:var(--mat-select-trigger-text-line-height, var(--mat-sys-body-large-line-height));font-size:var(--mat-select-trigger-text-size, var(--mat-sys-body-large-size));font-weight:var(--mat-select-trigger-text-weight, var(--mat-sys-body-large-weight));letter-spacing:var(--mat-select-trigger-text-tracking, var(--mat-sys-body-large-tracking))}div.mat-mdc-select-panel{box-shadow:var(--mat-select-container-elevation-shadow, 0px 3px 1px -2px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12))}.mat-mdc-select-disabled{color:var(--mat-select-disabled-trigger-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-mdc-select-disabled .mat-mdc-select-placeholder{color:var(--mat-select-disabled-trigger-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-mdc-select-trigger{display:inline-flex;align-items:center;cursor:pointer;position:relative;box-sizing:border-box;width:100%}.mat-mdc-select-disabled .mat-mdc-select-trigger{-webkit-user-select:none;user-select:none;cursor:default}.mat-mdc-select-value{width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.mat-mdc-select-value-text{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.mat-mdc-select-arrow-wrapper{height:24px;flex-shrink:0;display:inline-flex;align-items:center}.mat-form-field-appearance-fill .mdc-text-field--no-label .mat-mdc-select-arrow-wrapper{transform:none}.mat-mdc-form-field .mat-mdc-select.mat-mdc-select-invalid .mat-mdc-select-arrow,.mat-form-field-invalid:not(.mat-form-field-disabled) .mat-mdc-form-field-infix::after{color:var(--mat-select-invalid-arrow-color, var(--mat-sys-error))}.mat-mdc-select-arrow{width:10px;height:5px;position:relative;color:var(--mat-select-enabled-arrow-color, var(--mat-sys-on-surface-variant))}.mat-mdc-form-field.mat-focused .mat-mdc-select-arrow{color:var(--mat-select-focused-arrow-color, var(--mat-sys-primary))}.mat-mdc-form-field .mat-mdc-select.mat-mdc-select-disabled .mat-mdc-select-arrow{color:var(--mat-select-disabled-arrow-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-mdc-select-arrow svg{fill:currentColor;position:absolute;top:50%;left:50%;transform:translate(-50%, -50%)}@media(forced-colors: active){.mat-mdc-select-arrow svg{fill:CanvasText}.mat-mdc-select-disabled .mat-mdc-select-arrow svg{fill:GrayText}}div.mat-mdc-select-panel{width:100%;max-height:275px;outline:0;overflow:auto;padding:8px 0;border-radius:4px;box-sizing:border-box;position:static;background-color:var(--mat-select-panel-background-color, var(--mat-sys-surface-container))}@media(forced-colors: active){div.mat-mdc-select-panel{outline:solid 1px}}.cdk-overlay-pane:not(.mat-mdc-select-panel-above) div.mat-mdc-select-panel{border-top-left-radius:0;border-top-right-radius:0;transform-origin:top center}.mat-mdc-select-panel-above div.mat-mdc-select-panel{border-bottom-left-radius:0;border-bottom-right-radius:0;transform-origin:bottom center}div.mat-mdc-select-panel .mat-mdc-option{--mdc-list-list-item-container-color: var(--mat-select-panel-background-color)}.mat-mdc-select-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1);color:var(--mat-select-placeholder-text-color, var(--mat-sys-on-surface-variant))}.mat-form-field-no-animations .mat-mdc-select-placeholder,._mat-animation-noopable .mat-mdc-select-placeholder{transition:none}.mat-form-field-hide-placeholder .mat-mdc-select-placeholder{color:rgba(0,0,0,0);-webkit-text-fill-color:rgba(0,0,0,0);transition:none;display:block}.mat-mdc-form-field-type-mat-select:not(.mat-form-field-disabled) .mat-mdc-text-field-wrapper{cursor:pointer}.mat-mdc-form-field-type-mat-select.mat-form-field-appearance-fill .mat-mdc-floating-label{max-width:calc(100% - 18px)}.mat-mdc-form-field-type-mat-select.mat-form-field-appearance-fill .mdc-floating-label--float-above{max-width:calc(100%/0.75 - 24px)}.mat-mdc-form-field-type-mat-select.mat-form-field-appearance-outline .mdc-notched-outline__notch{max-width:calc(100% - 60px)}.mat-mdc-form-field-type-mat-select.mat-form-field-appearance-outline .mdc-text-field--label-floating .mdc-notched-outline__notch{max-width:calc(100% - 24px)}.mat-mdc-select-min-line:empty::before{content:" ";white-space:pre;width:1px;display:inline-block;visibility:hidden}.mat-form-field-appearance-fill .mat-mdc-select-arrow-wrapper{transform:var(--mat-select-arrow-transform, translateY(-8px))}'],encapsulation:2,data:{animation:[t2.transformPanel]},changeDetection:0})}return t})();var KE=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({providers:[n2],imports:[vg,hm,mA,$o,tn,hm,mA]})}return t})();var r2=["tooltip"],qk=20;var Vk=new F("mat-tooltip-scroll-strategy",{providedIn:"root",factory:()=>{let t=B(je);return()=>t.scrollStrategies.reposition({scrollThrottle:qk})}});function s2(t){return()=>t.scrollStrategies.reposition({scrollThrottle:qk})}var a2={provide:Vk,deps:[je],useFactory:s2};function I2(){return{showDelay:0,hideDelay:0,touchendHideDelay:1500}}var C2=new F("mat-tooltip-default-options",{providedIn:"root",factory:I2});var Pk="tooltip-panel",Zk=Qo({passive:!0}),B2=8,Q2=8,E2=24,c2=200,Bs=(()=>{class t{_elementRef=B(q);_ngZone=B(tA);_platform=B(ZA);_ariaDescriber=B(ik);_focusMonitor=B(Kt);_dir=B(Se);_injector=B(yA);_defaultOptions=B(C2,{optional:!0});_overlayRef;_tooltipInstance;_portal;_position="below";_positionAtOrigin=!1;_disabled=!1;_tooltipClass;_viewInitialized=!1;_pointerExitEventsInitialized=!1;_tooltipComponent=l2;_viewportMargin=8;_currentPosition;_cssClassPrefix="mat-mdc";_ariaDescriptionPending;_dirSubscribed=!1;get position(){return this._position}set position(A){A!==this._position&&(this._position=A,this._overlayRef&&(this._updatePosition(this._overlayRef),this._tooltipInstance?.show(0),this._overlayRef.updatePosition()))}get positionAtOrigin(){return this._positionAtOrigin}set positionAtOrigin(A){this._positionAtOrigin=be(A),this._detach(),this._overlayRef=null}get disabled(){return this._disabled}set disabled(A){let i=be(A);this._disabled!==i&&(this._disabled=i,i?this.hide(0):this._setupPointerEnterEventsIfNeeded(),this._syncAriaDescription(this.message))}get showDelay(){return this._showDelay}set showDelay(A){this._showDelay=ft(A)}_showDelay;get hideDelay(){return this._hideDelay}set hideDelay(A){this._hideDelay=ft(A),this._tooltipInstance&&(this._tooltipInstance._mouseLeaveHideDelay=this._hideDelay)}_hideDelay;touchGestures="auto";get message(){return this._message}set message(A){let i=this._message;this._message=A!=null?String(A).trim():"",!this._message&&this._isTooltipVisible()?this.hide(0):(this._setupPointerEnterEventsIfNeeded(),this._updateTooltipMessage()),this._syncAriaDescription(i)}_message="";get tooltipClass(){return this._tooltipClass}set tooltipClass(A){this._tooltipClass=A,this._tooltipInstance&&this._setTooltipClass(this._tooltipClass)}_passiveListeners=[];_touchstartTimeout=null;_destroyed=new U;_isDestroyed=!1;constructor(){let A=this._defaultOptions;A&&(this._showDelay=A.showDelay,this._hideDelay=A.hideDelay,A.position&&(this.position=A.position),A.positionAtOrigin&&(this.positionAtOrigin=A.positionAtOrigin),A.touchGestures&&(this.touchGestures=A.touchGestures),A.tooltipClass&&(this.tooltipClass=A.tooltipClass)),this._viewportMargin=B2}ngAfterViewInit(){this._viewInitialized=!0,this._setupPointerEnterEventsIfNeeded(),this._focusMonitor.monitor(this._elementRef).pipe(pA(this._destroyed)).subscribe(A=>{A?A==="keyboard"&&this._ngZone.run(()=>this.show()):this._ngZone.run(()=>this.hide(0))})}ngOnDestroy(){let A=this._elementRef.nativeElement;this._touchstartTimeout&&clearTimeout(this._touchstartTimeout),this._overlayRef&&(this._overlayRef.dispose(),this._tooltipInstance=null),this._passiveListeners.forEach(([i,o])=>{A.removeEventListener(i,o,Zk)}),this._passiveListeners.length=0,this._destroyed.next(),this._destroyed.complete(),this._isDestroyed=!0,this._ariaDescriber.removeDescription(A,this.message,"tooltip"),this._focusMonitor.stopMonitoring(A)}show(A=this.showDelay,i){if(this.disabled||!this.message||this._isTooltipVisible()){this._tooltipInstance?._cancelPendingAnimations();return}let o=this._createOverlay(i);this._detach(),this._portal=this._portal||new _i(this._tooltipComponent,this._injector.get(Qe));let n=this._tooltipInstance=o.attach(this._portal).instance;n._triggerElement=this._elementRef.nativeElement,n._mouseLeaveHideDelay=this._hideDelay,n.afterHidden().pipe(pA(this._destroyed)).subscribe(()=>this._detach()),this._setTooltipClass(this._tooltipClass),this._updateTooltipMessage(),n.show(A)}hide(A=this.hideDelay){let i=this._tooltipInstance;i&&(i.isVisible()?i.hide(A):(i._cancelPendingAnimations(),this._detach()))}toggle(A){this._isTooltipVisible()?this.hide():this.show(void 0,A)}_isTooltipVisible(){return!!this._tooltipInstance&&this._tooltipInstance.isVisible()}_createOverlay(A){if(this._overlayRef){let g=this._overlayRef.getConfig().positionStrategy;if((!this.positionAtOrigin||!A)&&g._origin instanceof q)return this._overlayRef;this._detach()}let i=this._injector.get(Ln).getAncestorScrollContainers(this._elementRef),o=this._injector.get(je),n=o.position().flexibleConnectedTo(this.positionAtOrigin?A||this._elementRef:this._elementRef).withTransformOriginOn(`.${this._cssClassPrefix}-tooltip`).withFlexibleDimensions(!1).withViewportMargin(this._viewportMargin).withScrollableContainers(i);return n.positionChanges.pipe(pA(this._destroyed)).subscribe(g=>{this._updateCurrentPositionClass(g.connectionPair),this._tooltipInstance&&g.scrollableViewProperties.isOverlayClipped&&this._tooltipInstance.isVisible()&&this._ngZone.run(()=>this.hide(0))}),this._overlayRef=o.create({direction:this._dir,positionStrategy:n,panelClass:`${this._cssClassPrefix}-${Pk}`,scrollStrategy:this._injector.get(Vk)()}),this._updatePosition(this._overlayRef),this._overlayRef.detachments().pipe(pA(this._destroyed)).subscribe(()=>this._detach()),this._overlayRef.outsidePointerEvents().pipe(pA(this._destroyed)).subscribe(()=>this._tooltipInstance?._handleBodyInteraction()),this._overlayRef.keydownEvents().pipe(pA(this._destroyed)).subscribe(g=>{this._isTooltipVisible()&&g.keyCode===27&&!ze(g)&&(g.preventDefault(),g.stopPropagation(),this._ngZone.run(()=>this.hide(0)))}),this._defaultOptions?.disableTooltipInteractivity&&this._overlayRef.addPanelClass(`${this._cssClassPrefix}-tooltip-panel-non-interactive`),this._dirSubscribed||(this._dirSubscribed=!0,this._dir.change.pipe(pA(this._destroyed)).subscribe(()=>{this._overlayRef&&this._updatePosition(this._overlayRef)})),this._overlayRef}_detach(){this._overlayRef&&this._overlayRef.hasAttached()&&this._overlayRef.detach(),this._tooltipInstance=null}_updatePosition(A){let i=A.getConfig().positionStrategy,o=this._getOrigin(),n=this._getOverlayPosition();i.withPositions([this._addOffset(b(b({},o.main),n.main)),this._addOffset(b(b({},o.fallback),n.fallback))])}_addOffset(A){let i=Q2,o=!this._dir||this._dir.value=="ltr";return A.originY==="top"?A.offsetY=-i:A.originY==="bottom"?A.offsetY=i:A.originX==="start"?A.offsetX=o?-i:i:A.originX==="end"&&(A.offsetX=o?i:-i),A}_getOrigin(){let A=!this._dir||this._dir.value=="ltr",i=this.position,o;i=="above"||i=="below"?o={originX:"center",originY:i=="above"?"top":"bottom"}:i=="before"||i=="left"&&A||i=="right"&&!A?o={originX:"start",originY:"center"}:(i=="after"||i=="right"&&A||i=="left"&&!A)&&(o={originX:"end",originY:"center"});let{x:n,y:g}=this._invertPosition(o.originX,o.originY);return{main:o,fallback:{originX:n,originY:g}}}_getOverlayPosition(){let A=!this._dir||this._dir.value=="ltr",i=this.position,o;i=="above"?o={overlayX:"center",overlayY:"bottom"}:i=="below"?o={overlayX:"center",overlayY:"top"}:i=="before"||i=="left"&&A||i=="right"&&!A?o={overlayX:"end",overlayY:"center"}:(i=="after"||i=="right"&&A||i=="left"&&!A)&&(o={overlayX:"start",overlayY:"center"});let{x:n,y:g}=this._invertPosition(o.overlayX,o.overlayY);return{main:o,fallback:{overlayX:n,overlayY:g}}}_updateTooltipMessage(){this._tooltipInstance&&(this._tooltipInstance.message=this.message,this._tooltipInstance._markForCheck(),Le(()=>{this._tooltipInstance&&this._overlayRef.updatePosition()},{injector:this._injector}))}_setTooltipClass(A){this._tooltipInstance&&(this._tooltipInstance.tooltipClass=A,this._tooltipInstance._markForCheck())}_invertPosition(A,i){return this.position==="above"||this.position==="below"?i==="top"?i="bottom":i==="bottom"&&(i="top"):A==="end"?A="start":A==="start"&&(A="end"),{x:A,y:i}}_updateCurrentPositionClass(A){let{overlayY:i,originX:o,originY:n}=A,g;if(i==="center"?this._dir&&this._dir.value==="rtl"?g=o==="end"?"left":"right":g=o==="start"?"left":"right":g=i==="bottom"&&n==="top"?"above":"below",g!==this._currentPosition){let r=this._overlayRef;if(r){let s=`${this._cssClassPrefix}-${Pk}-`;r.removePanelClass(s+this._currentPosition),r.addPanelClass(s+g)}this._currentPosition=g}}_setupPointerEnterEventsIfNeeded(){this._disabled||!this.message||!this._viewInitialized||this._passiveListeners.length||(this._platformSupportsMouseEvents()?this._passiveListeners.push(["mouseenter",A=>{this._setupPointerExitEventsIfNeeded();let i;A.x!==void 0&&A.y!==void 0&&(i=A),this.show(void 0,i)}]):this.touchGestures!=="off"&&(this._disableNativeGesturesIfNecessary(),this._passiveListeners.push(["touchstart",A=>{let i=A.targetTouches?.[0],o=i?{x:i.clientX,y:i.clientY}:void 0;this._setupPointerExitEventsIfNeeded(),this._touchstartTimeout&&clearTimeout(this._touchstartTimeout);let n=500;this._touchstartTimeout=setTimeout(()=>{this._touchstartTimeout=null,this.show(void 0,o)},this._defaultOptions?.touchLongPressShowDelay??n)}])),this._addListeners(this._passiveListeners))}_setupPointerExitEventsIfNeeded(){if(this._pointerExitEventsInitialized)return;this._pointerExitEventsInitialized=!0;let A=[];if(this._platformSupportsMouseEvents())A.push(["mouseleave",i=>{let o=i.relatedTarget;(!o||!this._overlayRef?.overlayElement.contains(o))&&this.hide()}],["wheel",i=>this._wheelListener(i)]);else if(this.touchGestures!=="off"){this._disableNativeGesturesIfNecessary();let i=()=>{this._touchstartTimeout&&clearTimeout(this._touchstartTimeout),this.hide(this._defaultOptions?.touchendHideDelay)};A.push(["touchend",i],["touchcancel",i])}this._addListeners(A),this._passiveListeners.push(...A)}_addListeners(A){A.forEach(([i,o])=>{this._elementRef.nativeElement.addEventListener(i,o,Zk)})}_platformSupportsMouseEvents(){return!this._platform.IOS&&!this._platform.ANDROID}_wheelListener(A){if(this._isTooltipVisible()){let i=this._injector.get(cA).elementFromPoint(A.clientX,A.clientY),o=this._elementRef.nativeElement;i!==o&&!o.contains(i)&&this.hide()}}_disableNativeGesturesIfNecessary(){let A=this.touchGestures;if(A!=="off"){let i=this._elementRef.nativeElement,o=i.style;(A==="on"||i.nodeName!=="INPUT"&&i.nodeName!=="TEXTAREA")&&(o.userSelect=o.msUserSelect=o.webkitUserSelect=o.MozUserSelect="none"),(A==="on"||!i.draggable)&&(o.webkitUserDrag="none"),o.touchAction="none",o.webkitTapHighlightColor="transparent"}}_syncAriaDescription(A){this._ariaDescriptionPending||(this._ariaDescriptionPending=!0,this._ariaDescriber.removeDescription(this._elementRef.nativeElement,A,"tooltip"),this._isDestroyed||Le({write:()=>{this._ariaDescriptionPending=!1,this.message&&!this.disabled&&this._ariaDescriber.describe(this._elementRef.nativeElement,this.message,"tooltip")}},{injector:this._injector}))}static \u0275fac=function(i){return new(i||t)};static \u0275dir=T({type:t,selectors:[["","matTooltip",""]],hostAttrs:[1,"mat-mdc-tooltip-trigger"],hostVars:2,hostBindings:function(i,o){i&2&&nA("mat-mdc-tooltip-disabled",o.disabled)},inputs:{position:[0,"matTooltipPosition","position"],positionAtOrigin:[0,"matTooltipPositionAtOrigin","positionAtOrigin"],disabled:[0,"matTooltipDisabled","disabled"],showDelay:[0,"matTooltipShowDelay","showDelay"],hideDelay:[0,"matTooltipHideDelay","hideDelay"],touchGestures:[0,"matTooltipTouchGestures","touchGestures"],message:[0,"matTooltip","message"],tooltipClass:[0,"matTooltipClass","tooltipClass"]},exportAs:["matTooltip"]})}return t})(),l2=(()=>{class t{_changeDetectorRef=B(KA);_elementRef=B(q);_isMultiline=!1;message;tooltipClass;_showTimeoutId;_hideTimeoutId;_triggerElement;_mouseLeaveHideDelay;_animationsDisabled;_tooltip;_closeOnInteraction=!1;_isVisible=!1;_onHide=new U;_showAnimation="mat-mdc-tooltip-show";_hideAnimation="mat-mdc-tooltip-hide";constructor(){let A=B(Ae,{optional:!0});this._animationsDisabled=A==="NoopAnimations"}show(A){this._hideTimeoutId!=null&&clearTimeout(this._hideTimeoutId),this._showTimeoutId=setTimeout(()=>{this._toggleVisibility(!0),this._showTimeoutId=void 0},A)}hide(A){this._showTimeoutId!=null&&clearTimeout(this._showTimeoutId),this._hideTimeoutId=setTimeout(()=>{this._toggleVisibility(!1),this._hideTimeoutId=void 0},A)}afterHidden(){return this._onHide}isVisible(){return this._isVisible}ngOnDestroy(){this._cancelPendingAnimations(),this._onHide.complete(),this._triggerElement=null}_handleBodyInteraction(){this._closeOnInteraction&&this.hide(0)}_markForCheck(){this._changeDetectorRef.markForCheck()}_handleMouseLeave({relatedTarget:A}){(!A||!this._triggerElement.contains(A))&&(this.isVisible()?this.hide(this._mouseLeaveHideDelay):this._finalizeAnimation(!1))}_onShow(){this._isMultiline=this._isTooltipMultiline(),this._markForCheck()}_isTooltipMultiline(){let A=this._elementRef.nativeElement.getBoundingClientRect();return A.height>E2&&A.width>=c2}_handleAnimationEnd({animationName:A}){(A===this._showAnimation||A===this._hideAnimation)&&this._finalizeAnimation(A===this._showAnimation)}_cancelPendingAnimations(){this._showTimeoutId!=null&&clearTimeout(this._showTimeoutId),this._hideTimeoutId!=null&&clearTimeout(this._hideTimeoutId),this._showTimeoutId=this._hideTimeoutId=void 0}_finalizeAnimation(A){A?this._closeOnInteraction=!0:this.isVisible()||this._onHide.next()}_toggleVisibility(A){let i=this._tooltip.nativeElement,o=this._showAnimation,n=this._hideAnimation;if(i.classList.remove(A?n:o),i.classList.add(A?o:n),this._isVisible!==A&&(this._isVisible=A,this._changeDetectorRef.markForCheck()),A&&!this._animationsDisabled&&typeof getComputedStyle=="function"){let g=getComputedStyle(i);(g.getPropertyValue("animation-duration")==="0s"||g.getPropertyValue("animation-name")==="none")&&(this._animationsDisabled=!0)}A&&this._onShow(),this._animationsDisabled&&(i.classList.add("_mat-animation-noopable"),this._finalizeAnimation(A))}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["mat-tooltip-component"]],viewQuery:function(i,o){if(i&1&&QA(r2,7),i&2){let n;$(n=AA())&&(o._tooltip=n.first)}},hostAttrs:["aria-hidden","true"],hostBindings:function(i,o){i&1&&G("mouseleave",function(g){return o._handleMouseLeave(g)})},decls:4,vars:4,consts:[["tooltip",""],[1,"mdc-tooltip","mat-mdc-tooltip",3,"animationend","ngClass"],[1,"mat-mdc-tooltip-surface","mdc-tooltip__surface"]],template:function(i,o){if(i&1){let n=rA();d(0,"div",1,0),G("animationend",function(r){return Y(n),J(o._handleAnimationEnd(r))}),d(2,"div",2),k(3),h()()}i&2&&(nA("mdc-tooltip--multiline",o._isMultiline),L("ngClass",o.tooltipClass),D(3),NA(o.message))},dependencies:[zt],styles:['.mat-mdc-tooltip{position:relative;transform:scale(0);display:inline-flex}.mat-mdc-tooltip::before{content:"";top:0;right:0;bottom:0;left:0;z-index:-1;position:absolute}.mat-mdc-tooltip-panel-below .mat-mdc-tooltip::before{top:-8px}.mat-mdc-tooltip-panel-above .mat-mdc-tooltip::before{bottom:-8px}.mat-mdc-tooltip-panel-right .mat-mdc-tooltip::before{left:-8px}.mat-mdc-tooltip-panel-left .mat-mdc-tooltip::before{right:-8px}.mat-mdc-tooltip._mat-animation-noopable{animation:none;transform:scale(1)}.mat-mdc-tooltip-surface{word-break:normal;overflow-wrap:anywhere;padding:4px 8px;min-width:40px;max-width:200px;min-height:24px;max-height:40vh;box-sizing:border-box;overflow:hidden;text-align:center;will-change:transform,opacity;background-color:var(--mdc-plain-tooltip-container-color, var(--mat-sys-inverse-surface));color:var(--mdc-plain-tooltip-supporting-text-color, var(--mat-sys-inverse-on-surface));border-radius:var(--mdc-plain-tooltip-container-shape, var(--mat-sys-corner-extra-small));font-family:var(--mdc-plain-tooltip-supporting-text-font, var(--mat-sys-body-small-font));font-size:var(--mdc-plain-tooltip-supporting-text-size, var(--mat-sys-body-small-size));font-weight:var(--mdc-plain-tooltip-supporting-text-weight, var(--mat-sys-body-small-weight));line-height:var(--mdc-plain-tooltip-supporting-text-line-height, var(--mat-sys-body-small-line-height));letter-spacing:var(--mdc-plain-tooltip-supporting-text-tracking, var(--mat-sys-body-small-tracking))}.mat-mdc-tooltip-surface::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid rgba(0,0,0,0);border-radius:inherit;content:"";pointer-events:none}.mdc-tooltip--multiline .mat-mdc-tooltip-surface{text-align:left}[dir=rtl] .mdc-tooltip--multiline .mat-mdc-tooltip-surface{text-align:right}.mat-mdc-tooltip-panel{line-height:normal}.mat-mdc-tooltip-panel.mat-mdc-tooltip-panel-non-interactive{pointer-events:none}@keyframes mat-mdc-tooltip-show{0%{opacity:0;transform:scale(0.8)}100%{opacity:1;transform:scale(1)}}@keyframes mat-mdc-tooltip-hide{0%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(0.8)}}.mat-mdc-tooltip-show{animation:mat-mdc-tooltip-show 150ms cubic-bezier(0, 0, 0.2, 1) forwards}.mat-mdc-tooltip-hide{animation:mat-mdc-tooltip-hide 75ms cubic-bezier(0.4, 0, 1, 1) forwards}'],encapsulation:2,changeDetection:0})}return t})();var UE=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({providers:[a2],imports:[sm,vg,mA,mA,$o]})}return t})();function d2(t,e){if(t&1&&(d(0,"mat-option",17),k(1),h()),t&2){let A=e.$implicit;L("value",A),D(),YA(" ",A," ")}}function h2(t,e){if(t&1){let A=rA();d(0,"mat-form-field",14)(1,"mat-select",16,0),G("selectionChange",function(o){Y(A);let n=y(2);return J(n._changePageSize(o.value))}),fe(3,d2,2,2,"mat-option",17,De),h(),d(5,"div",18),G("click",function(){Y(A);let o=_e(2);return J(o.open())}),h()()}if(t&2){let A=y(2);L("appearance",A._formFieldAppearance)("color",A.color),D(),L("value",A.pageSize)("disabled",A.disabled)("aria-labelledby",A._pageSizeLabelId)("panelClass",A.selectConfig.panelClass||"")("disableOptionCentering",A.selectConfig.disableOptionCentering),D(2),pe(A._displayedPageSizeOptions)}}function u2(t,e){if(t&1&&(d(0,"div",15),k(1),h()),t&2){let A=y(2);D(),NA(A.pageSize)}}function m2(t,e){if(t&1&&(d(0,"div",3)(1,"div",13),k(2),h(),x(3,h2,6,7,"mat-form-field",14)(4,u2,2,1,"div",15),h()),t&2){let A=y();D(),aA("id",A._pageSizeLabelId),D(),YA(" ",A._intl.itemsPerPageLabel," "),D(),_(A._displayedPageSizeOptions.length>1?3:-1),D(),_(A._displayedPageSizeOptions.length<=1?4:-1)}}function D2(t,e){if(t&1){let A=rA();d(0,"button",19),G("click",function(){Y(A);let o=y();return J(o._buttonClicked(0,o._previousButtonsDisabled()))}),At(),d(1,"svg",8),P(2,"path",20),h()()}if(t&2){let A=y();L("matTooltip",A._intl.firstPageLabel)("matTooltipDisabled",A._previousButtonsDisabled())("disabled",A._previousButtonsDisabled()),aA("aria-label",A._intl.firstPageLabel)}}function f2(t,e){if(t&1){let A=rA();d(0,"button",21),G("click",function(){Y(A);let o=y();return J(o._buttonClicked(o.getNumberOfPages()-1,o._nextButtonsDisabled()))}),At(),d(1,"svg",8),P(2,"path",22),h()()}if(t&2){let A=y();L("matTooltip",A._intl.lastPageLabel)("matTooltipDisabled",A._nextButtonsDisabled())("disabled",A._nextButtonsDisabled()),aA("aria-label",A._intl.lastPageLabel)}}var Ng=(()=>{class t{changes=new U;itemsPerPageLabel="Items per page:";nextPageLabel="Next page";previousPageLabel="Previous page";firstPageLabel="First page";lastPageLabel="Last page";getRangeLabel=(A,i,o)=>{if(o==0||i==0)return`0 of ${o}`;o=Math.max(o,0);let n=A*i,g=n<o?Math.min(n+i,o):n+i;return`${n+1} \u2013 ${g} of ${o}`};static \u0275fac=function(i){return new(i||t)};static \u0275prov=S({token:t,factory:t.\u0275fac,providedIn:"root"})}return t})();function p2(t){return t||new Ng}var w2={provide:Ng,deps:[[new Ig,new ia,Ng]],useFactory:p2},y2=50;var M2=new F("MAT_PAGINATOR_DEFAULT_OPTIONS"),_m=(()=>{class t{_intl=B(Ng);_changeDetectorRef=B(KA);_formFieldAppearance;_pageSizeLabelId=B(re).getId("mat-paginator-page-size-label-");_intlChanges;_isInitialized=!1;_initializedStream=new fi(1);color;get pageIndex(){return this._pageIndex}set pageIndex(A){this._pageIndex=Math.max(A||0,0),this._changeDetectorRef.markForCheck()}_pageIndex=0;get length(){return this._length}set length(A){this._length=A||0,this._changeDetectorRef.markForCheck()}_length=0;get pageSize(){return this._pageSize}set pageSize(A){this._pageSize=Math.max(A||0,0),this._updateDisplayedPageSizeOptions()}_pageSize;get pageSizeOptions(){return this._pageSizeOptions}set pageSizeOptions(A){this._pageSizeOptions=(A||[]).map(i=>de(i,0)),this._updateDisplayedPageSizeOptions()}_pageSizeOptions=[];hidePageSize=!1;showFirstLastButtons=!1;selectConfig={};disabled=!1;page=new z;_displayedPageSizeOptions;initialized=this._initializedStream;constructor(){let A=this._intl,i=B(M2,{optional:!0});if(this._intlChanges=A.changes.subscribe(()=>this._changeDetectorRef.markForCheck()),i){let{pageSize:o,pageSizeOptions:n,hidePageSize:g,showFirstLastButtons:r}=i;o!=null&&(this._pageSize=o),n!=null&&(this._pageSizeOptions=n),g!=null&&(this.hidePageSize=g),r!=null&&(this.showFirstLastButtons=r)}this._formFieldAppearance=i?.formFieldAppearance||"outline"}ngOnInit(){this._isInitialized=!0,this._updateDisplayedPageSizeOptions(),this._initializedStream.next()}ngOnDestroy(){this._initializedStream.complete(),this._intlChanges.unsubscribe()}nextPage(){this.hasNextPage()&&this._navigate(this.pageIndex+1)}previousPage(){this.hasPreviousPage()&&this._navigate(this.pageIndex-1)}firstPage(){this.hasPreviousPage()&&this._navigate(0)}lastPage(){this.hasNextPage()&&this._navigate(this.getNumberOfPages()-1)}hasPreviousPage(){return this.pageIndex>=1&&this.pageSize!=0}hasNextPage(){let A=this.getNumberOfPages()-1;return this.pageIndex<A&&this.pageSize!=0}getNumberOfPages(){return this.pageSize?Math.ceil(this.length/this.pageSize):0}_changePageSize(A){let i=this.pageIndex*this.pageSize,o=this.pageIndex;this.pageIndex=Math.floor(i/A)||0,this.pageSize=A,this._emitPageEvent(o)}_nextButtonsDisabled(){return this.disabled||!this.hasNextPage()}_previousButtonsDisabled(){return this.disabled||!this.hasPreviousPage()}_updateDisplayedPageSizeOptions(){this._isInitialized&&(this.pageSize||(this._pageSize=this.pageSizeOptions.length!=0?this.pageSizeOptions[0]:y2),this._displayedPageSizeOptions=this.pageSizeOptions.slice(),this._displayedPageSizeOptions.indexOf(this.pageSize)===-1&&this._displayedPageSizeOptions.push(this.pageSize),this._displayedPageSizeOptions.sort((A,i)=>A-i),this._changeDetectorRef.markForCheck())}_emitPageEvent(A){this.page.emit({previousPageIndex:A,pageIndex:this.pageIndex,pageSize:this.pageSize,length:this.length})}_navigate(A){let i=this.pageIndex;A!==i&&(this.pageIndex=A,this._emitPageEvent(i))}_buttonClicked(A,i){i||this._navigate(A)}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["mat-paginator"]],hostAttrs:["role","group",1,"mat-mdc-paginator"],inputs:{color:"color",pageIndex:[2,"pageIndex","pageIndex",de],length:[2,"length","length",de],pageSize:[2,"pageSize","pageSize",de],pageSizeOptions:"pageSizeOptions",hidePageSize:[2,"hidePageSize","hidePageSize",eA],showFirstLastButtons:[2,"showFirstLastButtons","showFirstLastButtons",eA],selectConfig:"selectConfig",disabled:[2,"disabled","disabled",eA]},outputs:{page:"page"},exportAs:["matPaginator"],decls:14,vars:12,consts:[["selectRef",""],[1,"mat-mdc-paginator-outer-container"],[1,"mat-mdc-paginator-container"],[1,"mat-mdc-paginator-page-size"],[1,"mat-mdc-paginator-range-actions"],["aria-live","polite",1,"mat-mdc-paginator-range-label"],["mat-icon-button","","type","button","matTooltipPosition","above","disabledInteractive","",1,"mat-mdc-paginator-navigation-first",3,"matTooltip","matTooltipDisabled","disabled"],["mat-icon-button","","type","button","matTooltipPosition","above","disabledInteractive","",1,"mat-mdc-paginator-navigation-previous",3,"click","matTooltip","matTooltipDisabled","disabled"],["viewBox","0 0 24 24","focusable","false","aria-hidden","true",1,"mat-mdc-paginator-icon"],["d","M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"],["mat-icon-button","","type","button","matTooltipPosition","above","disabledInteractive","",1,"mat-mdc-paginator-navigation-next",3,"click","matTooltip","matTooltipDisabled","disabled"],["d","M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"],["mat-icon-button","","type","button","matTooltipPosition","above","disabledInteractive","",1,"mat-mdc-paginator-navigation-last",3,"matTooltip","matTooltipDisabled","disabled"],[1,"mat-mdc-paginator-page-size-label"],[1,"mat-mdc-paginator-page-size-select",3,"appearance","color"],[1,"mat-mdc-paginator-page-size-value"],["hideSingleSelectionIndicator","",3,"selectionChange","value","disabled","aria-labelledby","panelClass","disableOptionCentering"],[3,"value"],[1,"mat-mdc-paginator-touch-target",3,"click"],["mat-icon-button","","type","button","matTooltipPosition","above","disabledInteractive","",1,"mat-mdc-paginator-navigation-first",3,"click","matTooltip","matTooltipDisabled","disabled"],["d","M18.41 16.59L13.82 12l4.59-4.59L17 6l-6 6 6 6zM6 6h2v12H6z"],["mat-icon-button","","type","button","matTooltipPosition","above","disabledInteractive","",1,"mat-mdc-paginator-navigation-last",3,"click","matTooltip","matTooltipDisabled","disabled"],["d","M5.59 7.41L10.18 12l-4.59 4.59L7 18l6-6-6-6zM16 6h2v12h-2z"]],template:function(i,o){i&1&&(d(0,"div",1)(1,"div",2),x(2,m2,5,4,"div",3),d(3,"div",4)(4,"div",5),k(5),h(),x(6,D2,3,4,"button",6),d(7,"button",7),G("click",function(){return o._buttonClicked(o.pageIndex-1,o._previousButtonsDisabled())}),At(),d(8,"svg",8),P(9,"path",9),h()(),Bg(),d(10,"button",10),G("click",function(){return o._buttonClicked(o.pageIndex+1,o._nextButtonsDisabled())}),At(),d(11,"svg",8),P(12,"path",11),h()(),x(13,f2,3,4,"button",12),h()()()),i&2&&(D(2),_(o.hidePageSize?-1:2),D(3),YA(" ",o._intl.getRangeLabel(o.pageIndex,o.pageSize,o.length)," "),D(),_(o.showFirstLastButtons?6:-1),D(),L("matTooltip",o._intl.previousPageLabel)("matTooltipDisabled",o._previousButtonsDisabled())("disabled",o._previousButtonsDisabled()),aA("aria-label",o._intl.previousPageLabel),D(3),L("matTooltip",o._intl.nextPageLabel)("matTooltipDisabled",o._nextButtonsDisabled())("disabled",o._nextButtonsDisabled()),aA("aria-label",o._intl.nextPageLabel),D(3),_(o.showFirstLastButtons?13:-1))},dependencies:[ho,Cs,Nn,RE,Bs],styles:[".mat-mdc-paginator{display:block;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;color:var(--mat-paginator-container-text-color, var(--mat-sys-on-surface));background-color:var(--mat-paginator-container-background-color, var(--mat-sys-surface));font-family:var(--mat-paginator-container-text-font, var(--mat-sys-body-small-font));line-height:var(--mat-paginator-container-text-line-height, var(--mat-sys-body-small-line-height));font-size:var(--mat-paginator-container-text-size, var(--mat-sys-body-small-size));font-weight:var(--mat-paginator-container-text-weight, var(--mat-sys-body-small-weight));letter-spacing:var(--mat-paginator-container-text-tracking, var(--mat-sys-body-small-tracking));--mat-form-field-container-height:var(--mat-paginator-form-field-container-height, 40px);--mat-form-field-container-vertical-padding:var(--mat-paginator-form-field-container-vertical-padding, 8px)}.mat-mdc-paginator .mat-mdc-select-value{font-size:var(--mat-paginator-select-trigger-text-size, var(--mat-sys-body-small-size))}.mat-mdc-paginator .mat-mdc-form-field-subscript-wrapper{display:none}.mat-mdc-paginator .mat-mdc-select{line-height:1.5}.mat-mdc-paginator-outer-container{display:flex}.mat-mdc-paginator-container{display:flex;align-items:center;justify-content:flex-end;padding:0 8px;flex-wrap:wrap;width:100%;min-height:var(--mat-paginator-container-size, 56px)}.mat-mdc-paginator-page-size{display:flex;align-items:baseline;margin-right:8px}[dir=rtl] .mat-mdc-paginator-page-size{margin-right:0;margin-left:8px}.mat-mdc-paginator-page-size-label{margin:0 4px}.mat-mdc-paginator-page-size-select{margin:0 4px;width:84px}.mat-mdc-paginator-range-label{margin:0 32px 0 24px}.mat-mdc-paginator-range-actions{display:flex;align-items:center}.mat-mdc-paginator-icon{display:inline-block;width:28px;fill:var(--mat-paginator-enabled-icon-color, var(--mat-sys-on-surface-variant))}.mat-mdc-icon-button[aria-disabled] .mat-mdc-paginator-icon{fill:var(--mat-paginator-disabled-icon-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}[dir=rtl] .mat-mdc-paginator-icon{transform:rotate(180deg)}@media(forced-colors: active){.mat-mdc-icon-button[disabled] .mat-mdc-paginator-icon,.mat-mdc-paginator-icon{fill:currentColor;fill:CanvasText}.mat-mdc-paginator-range-actions .mat-mdc-icon-button{outline:solid 1px}}.mat-mdc-paginator-touch-target{display:var(--mat-paginator-touch-target-display, block);position:absolute;top:50%;left:50%;width:84px;height:48px;background-color:rgba(0,0,0,0);transform:translate(-50%, -50%);cursor:pointer}"],encapsulation:2,changeDetection:0})}return t})(),zk=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({providers:[w2],imports:[Xo,KE,UE,_m]})}return t})();function k2(t,e){if(t&1){let A=rA();d(0,"div",1)(1,"button",2),G("click",function(){Y(A);let o=y();return J(o.action())}),k(2),h()()}if(t&2){let A=y();D(2),YA(" ",A.data.action," ")}}var b2=["label"];function F2(t,e){}var v2=Math.pow(2,31)-1,uI=class{_overlayRef;instance;containerInstance;_afterDismissed=new U;_afterOpened=new U;_onAction=new U;_durationTimeoutId;_dismissedByAction=!1;constructor(e,A){this._overlayRef=A,this.containerInstance=e,e._onExit.subscribe(()=>this._finishDismiss())}dismiss(){this._afterDismissed.closed||this.containerInstance.exit(),clearTimeout(this._durationTimeoutId)}dismissWithAction(){this._onAction.closed||(this._dismissedByAction=!0,this._onAction.next(),this._onAction.complete(),this.dismiss()),clearTimeout(this._durationTimeoutId)}closeWithAction(){this.dismissWithAction()}_dismissAfter(e){this._durationTimeoutId=setTimeout(()=>this.dismiss(),Math.min(e,v2))}_open(){this._afterOpened.closed||(this._afterOpened.next(),this._afterOpened.complete())}_finishDismiss(){this._overlayRef.dispose(),this._onAction.closed||this._onAction.complete(),this._afterDismissed.next({dismissedByAction:this._dismissedByAction}),this._afterDismissed.complete(),this._dismissedByAction=!1}afterDismissed(){return this._afterDismissed}afterOpened(){return this.containerInstance._onEnter}onAction(){return this._onAction}},jk=new F("MatSnackBarData"),Qs=class{politeness="assertive";announcementMessage="";viewContainerRef;duration=0;panelClass;direction;data=null;horizontalPosition="center";verticalPosition="bottom"},S2=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275dir=T({type:t,selectors:[["","matSnackBarLabel",""]],hostAttrs:[1,"mat-mdc-snack-bar-label","mdc-snackbar__label"]})}return t})(),N2=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275dir=T({type:t,selectors:[["","matSnackBarActions",""]],hostAttrs:[1,"mat-mdc-snack-bar-actions","mdc-snackbar__actions"]})}return t})(),G2=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275dir=T({type:t,selectors:[["","matSnackBarAction",""]],hostAttrs:[1,"mat-mdc-snack-bar-action","mdc-snackbar__action"]})}return t})(),L2=(()=>{class t{snackBarRef=B(uI);data=B(jk);constructor(){}action(){this.snackBarRef.dismissWithAction()}get hasAction(){return!!this.data.action}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["simple-snack-bar"]],hostAttrs:[1,"mat-mdc-simple-snack-bar"],exportAs:["matSnackBar"],decls:3,vars:2,consts:[["matSnackBarLabel",""],["matSnackBarActions",""],["mat-button","","matSnackBarAction","",3,"click"]],template:function(i,o){i&1&&(d(0,"div",0),k(1),h(),x(2,k2,3,1,"div",1)),i&2&&(D(),YA(" ",o.data.message,`
`),D(),_(o.hasAction?2:-1))},dependencies:[Et,S2,N2,G2],styles:[".mat-mdc-simple-snack-bar{display:flex}"],encapsulation:2,changeDetection:0})}return t})(),_2={snackBarState:lo("state",[li("void, hidden",Ue({transform:"scale(0.8)",opacity:0})),li("visible",Ue({transform:"scale(1)",opacity:1})),xt("* => visible",ti("150ms cubic-bezier(0, 0, 0.2, 1)")),xt("* => void, * => hidden",ti("75ms cubic-bezier(0.4, 0.0, 1, 1)",Ue({opacity:0})))])},K2=(()=>{class t extends _n{_ngZone=B(tA);_elementRef=B(q);_changeDetectorRef=B(KA);_platform=B(ZA);snackBarConfig=B(Qs);_document=B(cA);_trackedModals=new Set;_announceDelay=150;_announceTimeoutId;_destroyed=!1;_portalOutlet;_onAnnounce=new U;_onExit=new U;_onEnter=new U;_animationState="void";_live;_label;_role;_liveElementId=B(re).getId("mat-snack-bar-container-live-");constructor(){super();let A=this.snackBarConfig;A.politeness==="assertive"&&!A.announcementMessage?this._live="assertive":A.politeness==="off"?this._live="off":this._live="polite",this._platform.FIREFOX&&(this._live==="polite"&&(this._role="status"),this._live==="assertive"&&(this._role="alert"))}attachComponentPortal(A){this._assertNotAttached();let i=this._portalOutlet.attachComponentPortal(A);return this._afterPortalAttached(),i}attachTemplatePortal(A){this._assertNotAttached();let i=this._portalOutlet.attachTemplatePortal(A);return this._afterPortalAttached(),i}attachDomPortal=A=>{this._assertNotAttached();let i=this._portalOutlet.attachDomPortal(A);return this._afterPortalAttached(),i};onAnimationEnd(A){let{fromState:i,toState:o}=A;if((o==="void"&&i!=="void"||o==="hidden")&&this._completeExit(),o==="visible"){let n=this._onEnter;this._ngZone.run(()=>{n.next(),n.complete()})}}enter(){this._destroyed||(this._animationState="visible",this._changeDetectorRef.markForCheck(),this._changeDetectorRef.detectChanges(),this._screenReaderAnnounce())}exit(){return this._ngZone.run(()=>{this._animationState="hidden",this._changeDetectorRef.markForCheck(),this._elementRef.nativeElement.setAttribute("mat-exit",""),clearTimeout(this._announceTimeoutId)}),this._onExit}ngOnDestroy(){this._destroyed=!0,this._clearFromModals(),this._completeExit()}_completeExit(){queueMicrotask(()=>{this._onExit.next(),this._onExit.complete()})}_afterPortalAttached(){let A=this._elementRef.nativeElement,i=this.snackBarConfig.panelClass;i&&(Array.isArray(i)?i.forEach(g=>A.classList.add(g)):A.classList.add(i)),this._exposeToModals();let o=this._label.nativeElement,n="mdc-snackbar__label";o.classList.toggle(n,!o.querySelector(`.${n}`))}_exposeToModals(){let A=this._liveElementId,i=this._document.querySelectorAll('body > .cdk-overlay-container [aria-modal="true"]');for(let o=0;o<i.length;o++){let n=i[o],g=n.getAttribute("aria-owns");this._trackedModals.add(n),g?g.indexOf(A)===-1&&n.setAttribute("aria-owns",g+" "+A):n.setAttribute("aria-owns",A)}}_clearFromModals(){this._trackedModals.forEach(A=>{let i=A.getAttribute("aria-owns");if(i){let o=i.replace(this._liveElementId,"").trim();o.length>0?A.setAttribute("aria-owns",o):A.removeAttribute("aria-owns")}}),this._trackedModals.clear()}_assertNotAttached(){this._portalOutlet.hasAttached()}_screenReaderAnnounce(){this._announceTimeoutId||this._ngZone.runOutsideAngular(()=>{this._announceTimeoutId=setTimeout(()=>{let A=this._elementRef.nativeElement.querySelector("[aria-hidden]"),i=this._elementRef.nativeElement.querySelector("[aria-live]");if(A&&i){let o=null;this._platform.isBrowser&&document.activeElement instanceof HTMLElement&&A.contains(document.activeElement)&&(o=document.activeElement),A.removeAttribute("aria-hidden"),i.appendChild(A),o?.focus(),this._onAnnounce.next(),this._onAnnounce.complete()}},this._announceDelay)})}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["mat-snack-bar-container"]],viewQuery:function(i,o){if(i&1&&(QA(Ei,7),QA(b2,7)),i&2){let n;$(n=AA())&&(o._portalOutlet=n.first),$(n=AA())&&(o._label=n.first)}},hostAttrs:[1,"mdc-snackbar","mat-mdc-snack-bar-container"],hostVars:1,hostBindings:function(i,o){i&1&&Lh("@state.done",function(g){return o.onAnimationEnd(g)}),i&2&&Gh("@state",o._animationState)},features:[dA],decls:6,vars:3,consts:[["label",""],[1,"mdc-snackbar__surface","mat-mdc-snackbar-surface"],[1,"mat-mdc-snack-bar-label"],["aria-hidden","true"],["cdkPortalOutlet",""]],template:function(i,o){i&1&&(d(0,"div",1)(1,"div",2,0)(3,"div",3),x(4,F2,0,0,"ng-template",4),h(),P(5,"div"),h()()),i&2&&(D(5),aA("aria-live",o._live)("role",o._role)("id",o._liveElementId))},dependencies:[Ei],styles:[".mat-mdc-snack-bar-container{display:flex;align-items:center;justify-content:center;box-sizing:border-box;-webkit-tap-highlight-color:rgba(0,0,0,0);margin:8px}.mat-mdc-snack-bar-handset .mat-mdc-snack-bar-container{width:100vw}.mat-mdc-snackbar-surface{box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12);display:flex;align-items:center;justify-content:flex-start;box-sizing:border-box;padding-left:0;padding-right:8px}[dir=rtl] .mat-mdc-snackbar-surface{padding-right:0;padding-left:8px}.mat-mdc-snack-bar-container .mat-mdc-snackbar-surface{min-width:344px;max-width:672px}.mat-mdc-snack-bar-handset .mat-mdc-snackbar-surface{width:100%;min-width:0}@media(forced-colors: active){.mat-mdc-snackbar-surface{outline:solid 1px}}.mat-mdc-snack-bar-container .mat-mdc-snackbar-surface{color:var(--mdc-snackbar-supporting-text-color, var(--mat-sys-inverse-on-surface));border-radius:var(--mdc-snackbar-container-shape, var(--mat-sys-corner-extra-small));background-color:var(--mdc-snackbar-container-color, var(--mat-sys-inverse-surface))}.mdc-snackbar__label{width:100%;flex-grow:1;box-sizing:border-box;margin:0;padding:14px 8px 14px 16px}[dir=rtl] .mdc-snackbar__label{padding-left:8px;padding-right:16px}.mat-mdc-snack-bar-container .mdc-snackbar__label{font-family:var(--mdc-snackbar-supporting-text-font, var(--mat-sys-body-medium-font));font-size:var(--mdc-snackbar-supporting-text-size, var(--mat-sys-body-medium-size));font-weight:var(--mdc-snackbar-supporting-text-weight, var(--mat-sys-body-medium-weight));line-height:var(--mdc-snackbar-supporting-text-line-height, var(--mat-sys-body-medium-line-height))}.mat-mdc-snack-bar-actions{display:flex;flex-shrink:0;align-items:center;box-sizing:border-box}.mat-mdc-snack-bar-handset,.mat-mdc-snack-bar-container,.mat-mdc-snack-bar-label{flex:1 1 auto}.mat-mdc-snack-bar-container .mat-mdc-button.mat-mdc-snack-bar-action:not(:disabled).mat-unthemed{color:var(--mat-snack-bar-button-color, var(--mat-sys-inverse-primary))}.mat-mdc-snack-bar-container .mat-mdc-button.mat-mdc-snack-bar-action:not(:disabled){--mat-text-button-state-layer-color:currentColor;--mat-text-button-ripple-color:currentColor}.mat-mdc-snack-bar-container .mat-mdc-button.mat-mdc-snack-bar-action:not(:disabled) .mat-ripple-element{opacity:.1}"],encapsulation:2,data:{animation:[_2.snackBarState]}})}return t})();function U2(){return new Qs}var x2=new F("mat-snack-bar-default-options",{providedIn:"root",factory:U2}),Xk=(()=>{class t{_overlay=B(je);_live=B(DE);_injector=B(yA);_breakpointObserver=B(aE);_parentSnackBar=B(t,{optional:!0,skipSelf:!0});_defaultConfig=B(x2);_snackBarRefAtThisLevel=null;simpleSnackBarComponent=L2;snackBarContainerComponent=K2;handsetCssClass="mat-mdc-snack-bar-handset";get _openedSnackBarRef(){let A=this._parentSnackBar;return A?A._openedSnackBarRef:this._snackBarRefAtThisLevel}set _openedSnackBarRef(A){this._parentSnackBar?this._parentSnackBar._openedSnackBarRef=A:this._snackBarRefAtThisLevel=A}constructor(){}openFromComponent(A,i){return this._attach(A,i)}openFromTemplate(A,i){return this._attach(A,i)}open(A,i="",o){let n=b(b({},this._defaultConfig),o);return n.data={message:A,action:i},n.announcementMessage===A&&(n.announcementMessage=void 0),this.openFromComponent(this.simpleSnackBarComponent,n)}dismiss(){this._openedSnackBarRef&&this._openedSnackBarRef.dismiss()}ngOnDestroy(){this._snackBarRefAtThisLevel&&this._snackBarRefAtThisLevel.dismiss()}_attachSnackBarContainer(A,i){let o=i&&i.viewContainerRef&&i.viewContainerRef.injector,n=yA.create({parent:o||this._injector,providers:[{provide:Qs,useValue:i}]}),g=new _i(this.snackBarContainerComponent,i.viewContainerRef,n),r=A.attach(g);return r.instance.snackBarConfig=i,r.instance}_attach(A,i){let o=b(b(b({},new Qs),this._defaultConfig),i),n=this._createOverlay(o),g=this._attachSnackBarContainer(n,o),r=new uI(g,n);if(A instanceof ge){let s=new Qi(A,null,{$implicit:o.data,snackBarRef:r});r.instance=g.attachTemplatePortal(s)}else{let s=this._createInjector(o,r),a=new _i(A,void 0,s),Q=g.attachComponentPortal(a);r.instance=Q.instance}return this._breakpointObserver.observe(zR.HandsetPortrait).pipe(pA(n.detachments())).subscribe(s=>{n.overlayElement.classList.toggle(this.handsetCssClass,s.matches)}),o.announcementMessage&&g._onAnnounce.subscribe(()=>{this._live.announce(o.announcementMessage,o.politeness)}),this._animateSnackBar(r,o),this._openedSnackBarRef=r,this._openedSnackBarRef}_animateSnackBar(A,i){A.afterDismissed().subscribe(()=>{this._openedSnackBarRef==A&&(this._openedSnackBarRef=null),i.announcementMessage&&this._live.clear()}),this._openedSnackBarRef?(this._openedSnackBarRef.afterDismissed().subscribe(()=>{A.containerInstance.enter()}),this._openedSnackBarRef.dismiss()):A.containerInstance.enter(),i.duration&&i.duration>0&&A.afterOpened().subscribe(()=>A._dismissAfter(i.duration))}_createOverlay(A){let i=new Kn;i.direction=A.direction;let o=this._overlay.position().global(),n=A.direction==="rtl",g=A.horizontalPosition==="left"||A.horizontalPosition==="start"&&!n||A.horizontalPosition==="end"&&n,r=!g&&A.horizontalPosition!=="center";return g?o.left("0"):r?o.right("0"):o.centerHorizontally(),A.verticalPosition==="top"?o.top("0"):o.bottom("0"),i.positionStrategy=o,this._overlay.create(i)}_createInjector(A,i){let o=A&&A.viewContainerRef&&A.viewContainerRef.injector;return yA.create({parent:o||this._injector,providers:[{provide:uI,useValue:i},{provide:jk,useValue:A.data}]})}static \u0275fac=function(i){return new(i||t)};static \u0275prov=S({token:t,factory:t.\u0275fac,providedIn:"root"})}return t})();var Y2=function(){var t,e,A,i,o,n,g,r,s,a,Q,c=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},f=new Promise((I,C)=>{t=I}),m=I=>console.log(I);function p(I){throw I}function M(){var I=Q.buffer;A=new Int8Array(I),i=new Int16Array(I),n=new Uint8Array(I),o=new Int32Array(I),g=new Uint32Array(I),r=new Float32Array(I),s=new Float64Array(I),a=new BigInt64Array(I),new BigUint64Array(I)}c.agerrMessages=[],c.stderrMessages=[],e=I=>c.stderrMessages.push(I);var K=typeof TextDecoder<"u"?new TextDecoder:void 0,W=function(I){let C=arguments.length>1&&arguments[1]!==void 0?arguments[1]:0;for(var l=C+(arguments.length>2&&arguments[2]!==void 0?arguments[2]:NaN),u=C;I[u]&&!(u>=l);)++u;if(u-C>16&&I.buffer&&K)return K.decode(I.subarray(C,u));for(var w="";C<u;){var R=I[C++];if(128&R){var v=63&I[C++];if((224&R)!=192){var N=63&I[C++];if((R=(240&R)==224?(15&R)<<12|v<<6|N:(7&R)<<18|v<<12|N<<6|63&I[C++])<65536)w+=String.fromCharCode(R);else{var CA=R-65536;w+=String.fromCharCode(55296|CA>>10,56320|1023&CA)}}else w+=String.fromCharCode((31&R)<<6|v)}else w+=String.fromCharCode(R)}return w},DA=(I,C)=>I?W(n,I,C):"";class xA{constructor(C){this.excPtr=C,this.ptr=C-24}set_type(C){g[this.ptr+4>>2]=C}get_type(){return g[this.ptr+4>>2]}set_destructor(C){g[this.ptr+8>>2]=C}get_destructor(){return g[this.ptr+8>>2]}set_caught(C){C=C?1:0,A[this.ptr+12]=C}get_caught(){return A[this.ptr+12]!=0}set_rethrown(C){C=C?1:0,A[this.ptr+13]=C}get_rethrown(){return A[this.ptr+13]!=0}init(C,l){this.set_adjusted_ptr(0),this.set_type(C),this.set_destructor(l)}set_adjusted_ptr(C){g[this.ptr+16>>2]=C}get_adjusted_ptr(){return g[this.ptr+16>>2]}}var wA={isAbs:I=>I.charAt(0)==="/",splitPath:I=>/^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$/.exec(I).slice(1),normalizeArray:(I,C)=>{for(var l=0,u=I.length-1;u>=0;u--){var w=I[u];w==="."?I.splice(u,1):w===".."?(I.splice(u,1),l++):l&&(I.splice(u,1),l--)}if(C)for(;l;l--)I.unshift("..");return I},normalize:I=>{var C=wA.isAbs(I),l=I.substr(-1)==="/";return(I=wA.normalizeArray(I.split("/").filter(u=>!!u),!C).join("/"))||C||(I="."),I&&l&&(I+="/"),(C?"/":"")+I},dirname:I=>{var C=wA.splitPath(I),l=C[0],u=C[1];return l||u?(u&&(u=u.substr(0,u.length-1)),l+u):"."},basename:I=>{if(I==="/")return"/";var C=(I=(I=wA.normalize(I)).replace(/\/$/,"")).lastIndexOf("/");return C===-1?I:I.substr(C+1)},join:function(){for(var I=arguments.length,C=new Array(I),l=0;l<I;l++)C[l]=arguments[l];return wA.normalize(C.join("/"))},join2:(I,C)=>wA.normalize(I+"/"+C)},wt=I=>(wt=(()=>{if(typeof crypto=="object"&&typeof crypto.getRandomValues=="function")return C=>crypto.getRandomValues(C);p("initRandomDevice")})())(I),we={resolve:function(){for(var I="",C=!1,l=arguments.length-1;l>=-1&&!C;l--){var u=l>=0?l<0||arguments.length<=l?void 0:arguments[l]:E.cwd();if(typeof u!="string")throw new TypeError("Arguments to path.resolve must be strings");if(!u)return"";I=u+"/"+I,C=wA.isAbs(u)}return(C?"/":"")+(I=wA.normalizeArray(I.split("/").filter(w=>!!w),!C).join("/"))||"."},relative:(I,C)=>{function l(vA){for(var RA=0;RA<vA.length&&vA[RA]==="";RA++);for(var hA=vA.length-1;hA>=0&&vA[hA]==="";hA--);return RA>hA?[]:vA.slice(RA,hA-RA+1)}I=we.resolve(I).substr(1),C=we.resolve(C).substr(1);for(var u=l(I.split("/")),w=l(C.split("/")),R=Math.min(u.length,w.length),v=R,N=0;N<R;N++)if(u[N]!==w[N]){v=N;break}var CA=[];for(N=v;N<u.length;N++)CA.push("..");return(CA=CA.concat(w.slice(v))).join("/")}},Fe=[],he=I=>{for(var C=0,l=0;l<I.length;++l){var u=I.charCodeAt(l);u<=127?C++:u<=2047?C+=2:u>=55296&&u<=57343?(C+=4,++l):C+=3}return C},ui=(I,C,l,u)=>{if(!(u>0))return 0;for(var w=l,R=l+u-1,v=0;v<I.length;++v){var N=I.charCodeAt(v);if(N>=55296&&N<=57343&&(N=65536+((1023&N)<<10)|1023&I.charCodeAt(++v)),N<=127){if(l>=R)break;C[l++]=N}else if(N<=2047){if(l+1>=R)break;C[l++]=192|N>>6,C[l++]=128|63&N}else if(N<=65535){if(l+2>=R)break;C[l++]=224|N>>12,C[l++]=128|N>>6&63,C[l++]=128|63&N}else{if(l+3>=R)break;C[l++]=240|N>>18,C[l++]=128|N>>12&63,C[l++]=128|N>>6&63,C[l++]=128|63&N}}return C[l]=0,l-w};function bo(I,C,l){var u=l>0?l:he(I)+1,w=new Array(u),R=ui(I,w,0,w.length);return C&&(w.length=R),w}var Hi={ttys:[],init(){},shutdown(){},register(I,C){Hi.ttys[I]={input:[],output:[],ops:C},E.registerDevice(I,Hi.stream_ops)},stream_ops:{open(I){var C=Hi.ttys[I.node.rdev];if(!C)throw new E.ErrnoError(43);I.tty=C,I.seekable=!1},close(I){I.tty.ops.fsync(I.tty)},fsync(I){I.tty.ops.fsync(I.tty)},read(I,C,l,u,w){if(!I.tty||!I.tty.ops.get_char)throw new E.ErrnoError(60);for(var R=0,v=0;v<u;v++){var N;try{N=I.tty.ops.get_char(I.tty)}catch{throw new E.ErrnoError(29)}if(N===void 0&&R===0)throw new E.ErrnoError(6);if(N==null)break;R++,C[l+v]=N}return R&&(I.node.timestamp=Date.now()),R},write(I,C,l,u,w){if(!I.tty||!I.tty.ops.put_char)throw new E.ErrnoError(60);try{for(var R=0;R<u;R++)I.tty.ops.put_char(I.tty,C[l+R])}catch{throw new E.ErrnoError(29)}return u&&(I.node.timestamp=Date.now()),R}},default_tty_ops:{get_char:I=>(()=>{if(!Fe.length){var C=null;if(typeof window<"u"&&typeof window.prompt=="function"&&(C=window.prompt("Input: "))!==null&&(C+=`
`),!C)return null;Fe=bo(C,!0)}return Fe.shift()})(),put_char(I,C){C===null||C===10?(m(W(I.output)),I.output=[]):C!=0&&I.output.push(C)},fsync(I){I.output&&I.output.length>0&&(m(W(I.output)),I.output=[])},ioctl_tcgets:I=>({c_iflag:25856,c_oflag:5,c_cflag:191,c_lflag:35387,c_cc:[3,28,127,21,4,0,1,0,17,19,26,0,18,15,23,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}),ioctl_tcsets:(I,C,l)=>0,ioctl_tiocgwinsz:I=>[24,80]},default_tty1_ops:{put_char(I,C){C===null||C===10?(e(W(I.output)),I.output=[]):C!=0&&I.output.push(C)},fsync(I){I.output&&I.output.length>0&&(e(W(I.output)),I.output=[])}}},Ti=(I,C)=>Math.ceil(I/C)*C,Zg=I=>{I=Ti(I,65536);var C=He(65536,I);return C&&((l,u)=>{n.fill(0,l,l+u)})(C,I),C},JA={ops_table:null,mount:I=>JA.createNode(null,"/",16895,0),createNode(I,C,l,u){if(E.isBlkdev(l)||E.isFIFO(l))throw new E.ErrnoError(63);JA.ops_table||={dir:{node:{getattr:JA.node_ops.getattr,setattr:JA.node_ops.setattr,lookup:JA.node_ops.lookup,mknod:JA.node_ops.mknod,rename:JA.node_ops.rename,unlink:JA.node_ops.unlink,rmdir:JA.node_ops.rmdir,readdir:JA.node_ops.readdir,symlink:JA.node_ops.symlink},stream:{llseek:JA.stream_ops.llseek}},file:{node:{getattr:JA.node_ops.getattr,setattr:JA.node_ops.setattr},stream:{llseek:JA.stream_ops.llseek,read:JA.stream_ops.read,write:JA.stream_ops.write,allocate:JA.stream_ops.allocate,mmap:JA.stream_ops.mmap,msync:JA.stream_ops.msync}},link:{node:{getattr:JA.node_ops.getattr,setattr:JA.node_ops.setattr,readlink:JA.node_ops.readlink},stream:{}},chrdev:{node:{getattr:JA.node_ops.getattr,setattr:JA.node_ops.setattr},stream:E.chrdev_stream_ops}};var w=E.createNode(I,C,l,u);return E.isDir(w.mode)?(w.node_ops=JA.ops_table.dir.node,w.stream_ops=JA.ops_table.dir.stream,w.contents={}):E.isFile(w.mode)?(w.node_ops=JA.ops_table.file.node,w.stream_ops=JA.ops_table.file.stream,w.usedBytes=0,w.contents=null):E.isLink(w.mode)?(w.node_ops=JA.ops_table.link.node,w.stream_ops=JA.ops_table.link.stream):E.isChrdev(w.mode)&&(w.node_ops=JA.ops_table.chrdev.node,w.stream_ops=JA.ops_table.chrdev.stream),w.timestamp=Date.now(),I&&(I.contents[C]=w,I.timestamp=w.timestamp),w},getFileDataAsTypedArray:I=>I.contents?I.contents.subarray?I.contents.subarray(0,I.usedBytes):new Uint8Array(I.contents):new Uint8Array(0),expandFileStorage(I,C){var l=I.contents?I.contents.length:0;if(!(l>=C)){C=Math.max(C,l*(l<1048576?2:1.125)>>>0),l!=0&&(C=Math.max(C,256));var u=I.contents;I.contents=new Uint8Array(C),I.usedBytes>0&&I.contents.set(u.subarray(0,I.usedBytes),0)}},resizeFileStorage(I,C){if(I.usedBytes!=C)if(C==0)I.contents=null,I.usedBytes=0;else{var l=I.contents;I.contents=new Uint8Array(C),l&&I.contents.set(l.subarray(0,Math.min(C,I.usedBytes))),I.usedBytes=C}},node_ops:{getattr(I){var C={};return C.dev=E.isChrdev(I.mode)?I.id:1,C.ino=I.id,C.mode=I.mode,C.nlink=1,C.uid=0,C.gid=0,C.rdev=I.rdev,E.isDir(I.mode)?C.size=4096:E.isFile(I.mode)?C.size=I.usedBytes:E.isLink(I.mode)?C.size=I.link.length:C.size=0,C.atime=new Date(I.timestamp),C.mtime=new Date(I.timestamp),C.ctime=new Date(I.timestamp),C.blksize=4096,C.blocks=Math.ceil(C.size/C.blksize),C},setattr(I,C){C.mode!==void 0&&(I.mode=C.mode),C.timestamp!==void 0&&(I.timestamp=C.timestamp),C.size!==void 0&&JA.resizeFileStorage(I,C.size)},lookup(I,C){throw E.genericErrors[44]},mknod:(I,C,l,u)=>JA.createNode(I,C,l,u),rename(I,C,l){if(E.isDir(I.mode)){var u;try{u=E.lookupNode(C,l)}catch{}if(u)for(var w in u.contents)throw new E.ErrnoError(55)}delete I.parent.contents[I.name],I.parent.timestamp=Date.now(),I.name=l,C.contents[l]=I,C.timestamp=I.parent.timestamp},unlink(I,C){delete I.contents[C],I.timestamp=Date.now()},rmdir(I,C){var l=E.lookupNode(I,C);for(var u in l.contents)throw new E.ErrnoError(55);delete I.contents[C],I.timestamp=Date.now()},readdir(I){var C=[".",".."];for(var l of Object.keys(I.contents))C.push(l);return C},symlink(I,C,l){var u=JA.createNode(I,C,41471,0);return u.link=l,u},readlink(I){if(!E.isLink(I.mode))throw new E.ErrnoError(28);return I.link}},stream_ops:{read(I,C,l,u,w){var R=I.node.contents;if(w>=I.node.usedBytes)return 0;var v=Math.min(I.node.usedBytes-w,u);if(v>8&&R.subarray)C.set(R.subarray(w,w+v),l);else for(var N=0;N<v;N++)C[l+N]=R[w+N];return v},write(I,C,l,u,w,R){if(C.buffer===A.buffer&&(R=!1),!u)return 0;var v=I.node;if(v.timestamp=Date.now(),C.subarray&&(!v.contents||v.contents.subarray)){if(R)return v.contents=C.subarray(l,l+u),v.usedBytes=u,u;if(v.usedBytes===0&&w===0)return v.contents=C.slice(l,l+u),v.usedBytes=u,u;if(w+u<=v.usedBytes)return v.contents.set(C.subarray(l,l+u),w),u}if(JA.expandFileStorage(v,w+u),v.contents.subarray&&C.subarray)v.contents.set(C.subarray(l,l+u),w);else for(var N=0;N<u;N++)v.contents[w+N]=C[l+N];return v.usedBytes=Math.max(v.usedBytes,w+u),u},llseek(I,C,l){var u=C;if(l===1?u+=I.position:l===2&&E.isFile(I.node.mode)&&(u+=I.node.usedBytes),u<0)throw new E.ErrnoError(28);return u},allocate(I,C,l){JA.expandFileStorage(I.node,C+l),I.node.usedBytes=Math.max(I.node.usedBytes,C+l)},mmap(I,C,l,u,w){if(!E.isFile(I.node.mode))throw new E.ErrnoError(43);var R,v,N=I.node.contents;if(2&w||!N||N.buffer!==A.buffer){if(v=!0,!(R=Zg(C)))throw new E.ErrnoError(48);N&&((l>0||l+C<N.length)&&(N=N.subarray?N.subarray(l,l+C):Array.prototype.slice.call(N,l,l+C)),A.set(N,R))}else v=!1,R=N.byteOffset;return{ptr:R,allocated:v}},msync:(I,C,l,u,w)=>(JA.stream_ops.write(I,C,0,u,l,!1),0)}},qg=(I,C)=>{var l=0;return I&&(l|=365),C&&(l|=146),l},E={root:null,mounts:[],devices:{},streams:[],nextInode:1,nameTable:null,currentPath:"/",initialized:!1,ignorePermissions:!0,ErrnoError:class{constructor(I){this.name="ErrnoError",this.errno=I}},genericErrors:{},filesystems:null,syncFSRequests:0,FSStream:class{constructor(){this.shared={}}get object(){return this.node}set object(I){this.node=I}get isRead(){return(2097155&this.flags)!=1}get isWrite(){return!!(2097155&this.flags)}get isAppend(){return 1024&this.flags}get flags(){return this.shared.flags}set flags(I){this.shared.flags=I}get position(){return this.shared.position}set position(I){this.shared.position=I}},FSNode:class{constructor(I,C,l,u){I||(I=this),this.parent=I,this.mount=I.mount,this.mounted=null,this.id=E.nextInode++,this.name=C,this.mode=l,this.node_ops={},this.stream_ops={},this.rdev=u,this.readMode=365,this.writeMode=146}get read(){return(this.mode&this.readMode)===this.readMode}set read(I){I?this.mode|=this.readMode:this.mode&=~this.readMode}get write(){return(this.mode&this.writeMode)===this.writeMode}set write(I){I?this.mode|=this.writeMode:this.mode&=~this.writeMode}get isFolder(){return E.isDir(this.mode)}get isDevice(){return E.isChrdev(this.mode)}},lookupPath(I){let C=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};if(!(I=we.resolve(I)))return{path:"",node:null};if(C=Object.assign({follow_mount:!0,recurse_count:0},C),C.recurse_count>8)throw new E.ErrnoError(32);for(var l=I.split("/").filter(vA=>!!vA),u=E.root,w="/",R=0;R<l.length;R++){var v=R===l.length-1;if(v&&C.parent)break;if(u=E.lookupNode(u,l[R]),w=wA.join2(w,l[R]),E.isMountpoint(u)&&(!v||v&&C.follow_mount)&&(u=u.mounted.root),!v||C.follow)for(var N=0;E.isLink(u.mode);){var CA=E.readlink(w);if(w=we.resolve(wA.dirname(w),CA),u=E.lookupPath(w,{recurse_count:C.recurse_count+1}).node,N++>40)throw new E.ErrnoError(32)}}return{path:w,node:u}},getPath(I){for(var C;;){if(E.isRoot(I)){var l=I.mount.mountpoint;return C?l[l.length-1]!=="/"?`${l}/${C}`:l+C:l}C=C?`${I.name}/${C}`:I.name,I=I.parent}},hashName(I,C){for(var l=0,u=0;u<C.length;u++)l=(l<<5)-l+C.charCodeAt(u)|0;return(I+l>>>0)%E.nameTable.length},hashAddNode(I){var C=E.hashName(I.parent.id,I.name);I.name_next=E.nameTable[C],E.nameTable[C]=I},hashRemoveNode(I){var C=E.hashName(I.parent.id,I.name);if(E.nameTable[C]===I)E.nameTable[C]=I.name_next;else for(var l=E.nameTable[C];l;){if(l.name_next===I){l.name_next=I.name_next;break}l=l.name_next}},lookupNode(I,C){var l=E.mayLookup(I);if(l)throw new E.ErrnoError(l);for(var u=E.hashName(I.id,C),w=E.nameTable[u];w;w=w.name_next){var R=w.name;if(w.parent.id===I.id&&R===C)return w}return E.lookup(I,C)},createNode(I,C,l,u){var w=new E.FSNode(I,C,l,u);return E.hashAddNode(w),w},destroyNode(I){E.hashRemoveNode(I)},isRoot:I=>I===I.parent,isMountpoint:I=>!!I.mounted,isFile:I=>(61440&I)==32768,isDir:I=>(61440&I)==16384,isLink:I=>(61440&I)==40960,isChrdev:I=>(61440&I)==8192,isBlkdev:I=>(61440&I)==24576,isFIFO:I=>(61440&I)==4096,isSocket:I=>!(49152&~I),flagsToPermissionString(I){var C=["r","w","rw"][3&I];return 512&I&&(C+="w"),C},nodePermissions:(I,C)=>E.ignorePermissions||(!C.includes("r")||292&I.mode)&&(!C.includes("w")||146&I.mode)&&(!C.includes("x")||73&I.mode)?0:2,mayLookup(I){if(!E.isDir(I.mode))return 54;var C=E.nodePermissions(I,"x");return C||(I.node_ops.lookup?0:2)},mayCreate(I,C){try{return E.lookupNode(I,C),20}catch{}return E.nodePermissions(I,"wx")},mayDelete(I,C,l){var u;try{u=E.lookupNode(I,C)}catch(R){return R.errno}var w=E.nodePermissions(I,"wx");if(w)return w;if(l){if(!E.isDir(u.mode))return 54;if(E.isRoot(u)||E.getPath(u)===E.cwd())return 10}else if(E.isDir(u.mode))return 31;return 0},mayOpen:(I,C)=>I?E.isLink(I.mode)?32:E.isDir(I.mode)&&(E.flagsToPermissionString(C)!=="r"||512&C)?31:E.nodePermissions(I,E.flagsToPermissionString(C)):44,MAX_OPEN_FDS:4096,nextfd(){for(var I=0;I<=E.MAX_OPEN_FDS;I++)if(!E.streams[I])return I;throw new E.ErrnoError(33)},getStreamChecked(I){var C=E.getStream(I);if(!C)throw new E.ErrnoError(8);return C},getStream:I=>E.streams[I],createStream(I){let C=arguments.length>1&&arguments[1]!==void 0?arguments[1]:-1;return I=Object.assign(new E.FSStream,I),C==-1&&(C=E.nextfd()),I.fd=C,E.streams[C]=I,I},closeStream(I){E.streams[I]=null},dupStream(I){let C=arguments.length>1&&arguments[1]!==void 0?arguments[1]:-1;var l=E.createStream(I,C);return l.stream_ops?.dup?.(l),l},chrdev_stream_ops:{open(I){var C=E.getDevice(I.node.rdev);I.stream_ops=C.stream_ops,I.stream_ops.open?.(I)},llseek(){throw new E.ErrnoError(70)}},major:I=>I>>8,minor:I=>255&I,makedev:(I,C)=>I<<8|C,registerDevice(I,C){E.devices[I]={stream_ops:C}},getDevice:I=>E.devices[I],getMounts(I){for(var C=[],l=[I];l.length;){var u=l.pop();C.push(u),l.push(...u.mounts)}return C},syncfs(I,C){typeof I=="function"&&(C=I,I=!1),E.syncFSRequests++,E.syncFSRequests>1&&e(`warning: ${E.syncFSRequests} FS.syncfs operations in flight at once, probably just doing extra work`);var l=E.getMounts(E.root.mount),u=0;function w(v){return E.syncFSRequests--,C(v)}function R(v){if(v)return R.errored?void 0:(R.errored=!0,w(v));++u>=l.length&&w(null)}l.forEach(v=>{if(!v.type.syncfs)return R(null);v.type.syncfs(v,I,R)})},mount(I,C,l){var u,w=l==="/",R=!l;if(w&&E.root)throw new E.ErrnoError(10);if(!w&&!R){var v=E.lookupPath(l,{follow_mount:!1});if(l=v.path,u=v.node,E.isMountpoint(u))throw new E.ErrnoError(10);if(!E.isDir(u.mode))throw new E.ErrnoError(54)}var N={type:I,opts:C,mountpoint:l,mounts:[]},CA=I.mount(N);return CA.mount=N,N.root=CA,w?E.root=CA:u&&(u.mounted=N,u.mount&&u.mount.mounts.push(N)),CA},unmount(I){var C=E.lookupPath(I,{follow_mount:!1});if(!E.isMountpoint(C.node))throw new E.ErrnoError(28);var l=C.node,u=l.mounted,w=E.getMounts(u);Object.keys(E.nameTable).forEach(v=>{for(var N=E.nameTable[v];N;){var CA=N.name_next;w.includes(N.mount)&&E.destroyNode(N),N=CA}}),l.mounted=null;var R=l.mount.mounts.indexOf(u);l.mount.mounts.splice(R,1)},lookup:(I,C)=>I.node_ops.lookup(I,C),mknod(I,C,l){var u=E.lookupPath(I,{parent:!0}).node,w=wA.basename(I);if(!w||w==="."||w==="..")throw new E.ErrnoError(28);var R=E.mayCreate(u,w);if(R)throw new E.ErrnoError(R);if(!u.node_ops.mknod)throw new E.ErrnoError(63);return u.node_ops.mknod(u,w,C,l)},create:(I,C)=>(C=C!==void 0?C:438,C&=4095,C|=32768,E.mknod(I,C,0)),mkdir:(I,C)=>(C=C!==void 0?C:511,C&=1023,C|=16384,E.mknod(I,C,0)),mkdirTree(I,C){for(var l=I.split("/"),u="",w=0;w<l.length;++w)if(l[w]){u+="/"+l[w];try{E.mkdir(u,C)}catch(R){if(R.errno!=20)throw R}}},mkdev:(I,C,l)=>(l===void 0&&(l=C,C=438),C|=8192,E.mknod(I,C,l)),symlink(I,C){if(!we.resolve(I))throw new E.ErrnoError(44);var l=E.lookupPath(C,{parent:!0}).node;if(!l)throw new E.ErrnoError(44);var u=wA.basename(C),w=E.mayCreate(l,u);if(w)throw new E.ErrnoError(w);if(!l.node_ops.symlink)throw new E.ErrnoError(63);return l.node_ops.symlink(l,u,I)},rename(I,C){var l,u,w=wA.dirname(I),R=wA.dirname(C),v=wA.basename(I),N=wA.basename(C);if(l=E.lookupPath(I,{parent:!0}).node,u=E.lookupPath(C,{parent:!0}).node,!l||!u)throw new E.ErrnoError(44);if(l.mount!==u.mount)throw new E.ErrnoError(75);var CA,vA=E.lookupNode(l,v),RA=we.relative(I,R);if(RA.charAt(0)!==".")throw new E.ErrnoError(28);if((RA=we.relative(C,w)).charAt(0)!==".")throw new E.ErrnoError(55);try{CA=E.lookupNode(u,N)}catch{}if(vA!==CA){var hA=E.isDir(vA.mode),EA=E.mayDelete(l,v,hA);if(EA)throw new E.ErrnoError(EA);if(EA=CA?E.mayDelete(u,N,hA):E.mayCreate(u,N))throw new E.ErrnoError(EA);if(!l.node_ops.rename)throw new E.ErrnoError(63);if(E.isMountpoint(vA)||CA&&E.isMountpoint(CA))throw new E.ErrnoError(10);if(u!==l&&(EA=E.nodePermissions(l,"w")))throw new E.ErrnoError(EA);E.hashRemoveNode(vA);try{l.node_ops.rename(vA,u,N),vA.parent=u}catch(lA){throw lA}finally{E.hashAddNode(vA)}}},rmdir(I){var C=E.lookupPath(I,{parent:!0}).node,l=wA.basename(I),u=E.lookupNode(C,l),w=E.mayDelete(C,l,!0);if(w)throw new E.ErrnoError(w);if(!C.node_ops.rmdir)throw new E.ErrnoError(63);if(E.isMountpoint(u))throw new E.ErrnoError(10);C.node_ops.rmdir(C,l),E.destroyNode(u)},readdir(I){var C=E.lookupPath(I,{follow:!0}).node;if(!C.node_ops.readdir)throw new E.ErrnoError(54);return C.node_ops.readdir(C)},unlink(I){var C=E.lookupPath(I,{parent:!0}).node;if(!C)throw new E.ErrnoError(44);var l=wA.basename(I),u=E.lookupNode(C,l),w=E.mayDelete(C,l,!1);if(w)throw new E.ErrnoError(w);if(!C.node_ops.unlink)throw new E.ErrnoError(63);if(E.isMountpoint(u))throw new E.ErrnoError(10);C.node_ops.unlink(C,l),E.destroyNode(u)},readlink(I){var C=E.lookupPath(I).node;if(!C)throw new E.ErrnoError(44);if(!C.node_ops.readlink)throw new E.ErrnoError(28);return we.resolve(E.getPath(C.parent),C.node_ops.readlink(C))},stat(I,C){var l=E.lookupPath(I,{follow:!C}).node;if(!l)throw new E.ErrnoError(44);if(!l.node_ops.getattr)throw new E.ErrnoError(63);return l.node_ops.getattr(l)},lstat:I=>E.stat(I,!0),chmod(I,C,l){var u;if(typeof I=="string"?u=E.lookupPath(I,{follow:!l}).node:u=I,!u.node_ops.setattr)throw new E.ErrnoError(63);u.node_ops.setattr(u,{mode:4095&C|-4096&u.mode,timestamp:Date.now()})},lchmod(I,C){E.chmod(I,C,!0)},fchmod(I,C){var l=E.getStreamChecked(I);E.chmod(l.node,C)},chown(I,C,l,u){var w;if(typeof I=="string"?w=E.lookupPath(I,{follow:!u}).node:w=I,!w.node_ops.setattr)throw new E.ErrnoError(63);w.node_ops.setattr(w,{timestamp:Date.now()})},lchown(I,C,l){E.chown(I,C,l,!0)},fchown(I,C,l){var u=E.getStreamChecked(I);E.chown(u.node,C,l)},truncate(I,C){if(C<0)throw new E.ErrnoError(28);var l;if(typeof I=="string"?l=E.lookupPath(I,{follow:!0}).node:l=I,!l.node_ops.setattr)throw new E.ErrnoError(63);if(E.isDir(l.mode))throw new E.ErrnoError(31);if(!E.isFile(l.mode))throw new E.ErrnoError(28);var u=E.nodePermissions(l,"w");if(u)throw new E.ErrnoError(u);l.node_ops.setattr(l,{size:C,timestamp:Date.now()})},ftruncate(I,C){var l=E.getStreamChecked(I);if(!(2097155&l.flags))throw new E.ErrnoError(28);E.truncate(l.node,C)},utime(I,C,l){var u=E.lookupPath(I,{follow:!0}).node;u.node_ops.setattr(u,{timestamp:Math.max(C,l)})},open(I,C,l){if(I==="")throw new E.ErrnoError(44);var u;if(l=64&(C=typeof C=="string"?(N=>{var CA={r:0,"r+":2,w:577,"w+":578,a:1089,"a+":1090}[N];if(CA===void 0)throw new Error(`Unknown file open mode: ${N}`);return CA})(C):C)?4095&(l=l===void 0?438:l)|32768:0,typeof I=="object")u=I;else{I=wA.normalize(I);try{u=E.lookupPath(I,{follow:!(131072&C)}).node}catch{}}var w=!1;if(64&C)if(u){if(128&C)throw new E.ErrnoError(20)}else u=E.mknod(I,l,0),w=!0;if(!u)throw new E.ErrnoError(44);if(E.isChrdev(u.mode)&&(C&=-513),65536&C&&!E.isDir(u.mode))throw new E.ErrnoError(54);if(!w){var R=E.mayOpen(u,C);if(R)throw new E.ErrnoError(R)}512&C&&!w&&E.truncate(u,0),C&=-131713;var v=E.createStream({node:u,path:E.getPath(u),flags:C,seekable:!0,position:0,stream_ops:u.stream_ops,ungotten:[],error:!1});return v.stream_ops.open&&v.stream_ops.open(v),v},close(I){if(E.isClosed(I))throw new E.ErrnoError(8);I.getdents&&(I.getdents=null);try{I.stream_ops.close&&I.stream_ops.close(I)}catch(C){throw C}finally{E.closeStream(I.fd)}I.fd=null},isClosed:I=>I.fd===null,llseek(I,C,l){if(E.isClosed(I))throw new E.ErrnoError(8);if(!I.seekable||!I.stream_ops.llseek)throw new E.ErrnoError(70);if(l!=0&&l!=1&&l!=2)throw new E.ErrnoError(28);return I.position=I.stream_ops.llseek(I,C,l),I.ungotten=[],I.position},read(I,C,l,u,w){if(u<0||w<0)throw new E.ErrnoError(28);if(E.isClosed(I))throw new E.ErrnoError(8);if((2097155&I.flags)==1)throw new E.ErrnoError(8);if(E.isDir(I.node.mode))throw new E.ErrnoError(31);if(!I.stream_ops.read)throw new E.ErrnoError(28);var R=w!==void 0;if(R){if(!I.seekable)throw new E.ErrnoError(70)}else w=I.position;var v=I.stream_ops.read(I,C,l,u,w);return R||(I.position+=v),v},write(I,C,l,u,w,R){if(u<0||w<0)throw new E.ErrnoError(28);if(E.isClosed(I))throw new E.ErrnoError(8);if(!(2097155&I.flags))throw new E.ErrnoError(8);if(E.isDir(I.node.mode))throw new E.ErrnoError(31);if(!I.stream_ops.write)throw new E.ErrnoError(28);I.seekable&&1024&I.flags&&E.llseek(I,0,2);var v=w!==void 0;if(v){if(!I.seekable)throw new E.ErrnoError(70)}else w=I.position;var N=I.stream_ops.write(I,C,l,u,w,R);return v||(I.position+=N),N},allocate(I,C,l){if(E.isClosed(I))throw new E.ErrnoError(8);if(C<0||l<=0)throw new E.ErrnoError(28);if(!(2097155&I.flags))throw new E.ErrnoError(8);if(!E.isFile(I.node.mode)&&!E.isDir(I.node.mode))throw new E.ErrnoError(43);if(!I.stream_ops.allocate)throw new E.ErrnoError(138);I.stream_ops.allocate(I,C,l)},mmap(I,C,l,u,w){if(2&u&&!(2&w)&&(2097155&I.flags)!=2)throw new E.ErrnoError(2);if((2097155&I.flags)==1)throw new E.ErrnoError(2);if(!I.stream_ops.mmap)throw new E.ErrnoError(43);if(!C)throw new E.ErrnoError(28);return I.stream_ops.mmap(I,C,l,u,w)},msync:(I,C,l,u,w)=>I.stream_ops.msync?I.stream_ops.msync(I,C,l,u,w):0,ioctl(I,C,l){if(!I.stream_ops.ioctl)throw new E.ErrnoError(59);return I.stream_ops.ioctl(I,C,l)},readFile(I){let C=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};if(C.flags=C.flags||0,C.encoding=C.encoding||"binary",C.encoding!=="utf8"&&C.encoding!=="binary")throw new Error(`Invalid encoding type "${C.encoding}"`);var l,u=E.open(I,C.flags),w=E.stat(I).size,R=new Uint8Array(w);return E.read(u,R,0,w,0),C.encoding==="utf8"?l=W(R):C.encoding==="binary"&&(l=R),E.close(u),l},writeFile(I,C){let l=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};l.flags=l.flags||577;var u=E.open(I,l.flags,l.mode);if(typeof C=="string"){var w=new Uint8Array(he(C)+1),R=ui(C,w,0,w.length);E.write(u,w,0,R,void 0,l.canOwn)}else{if(!ArrayBuffer.isView(C))throw new Error("Unsupported data type");E.write(u,C,0,C.byteLength,void 0,l.canOwn)}E.close(u)},cwd:()=>E.currentPath,chdir(I){var C=E.lookupPath(I,{follow:!0});if(C.node===null)throw new E.ErrnoError(44);if(!E.isDir(C.node.mode))throw new E.ErrnoError(54);var l=E.nodePermissions(C.node,"x");if(l)throw new E.ErrnoError(l);E.currentPath=C.path},createDefaultDirectories(){E.mkdir("/tmp"),E.mkdir("/home"),E.mkdir("/home/web_user")},createDefaultDevices(){E.mkdir("/dev"),E.registerDevice(E.makedev(1,3),{read:()=>0,write:(u,w,R,v,N)=>v}),E.mkdev("/dev/null",E.makedev(1,3)),Hi.register(E.makedev(5,0),Hi.default_tty_ops),Hi.register(E.makedev(6,0),Hi.default_tty1_ops),E.mkdev("/dev/tty",E.makedev(5,0)),E.mkdev("/dev/tty1",E.makedev(6,0));var I=new Uint8Array(1024),C=0,l=()=>(C===0&&(C=wt(I).byteLength),I[--C]);E.createDevice("/dev","random",l),E.createDevice("/dev","urandom",l),E.mkdir("/dev/shm"),E.mkdir("/dev/shm/tmp")},createSpecialDirectories(){E.mkdir("/proc");var I=E.mkdir("/proc/self");E.mkdir("/proc/self/fd"),E.mount({mount(){var C=E.createNode(I,"fd",16895,73);return C.node_ops={lookup(l,u){var w=+u,R=E.getStreamChecked(w),v={parent:null,mount:{mountpoint:"fake"},node_ops:{readlink:()=>R.path}};return v.parent=v,v}},C}},{},"/proc/self/fd")},createStandardStreams(I,C,l){I?E.createDevice("/dev","stdin",I):E.symlink("/dev/tty","/dev/stdin"),C?E.createDevice("/dev","stdout",null,C):E.symlink("/dev/tty","/dev/stdout"),l?E.createDevice("/dev","stderr",null,l):E.symlink("/dev/tty1","/dev/stderr"),E.open("/dev/stdin",0),E.open("/dev/stdout",1),E.open("/dev/stderr",1)},staticInit(){[44].forEach(I=>{E.genericErrors[I]=new E.ErrnoError(I),E.genericErrors[I].stack="<generic error, no stack>"}),E.nameTable=new Array(4096),E.mount(JA,{},"/"),E.createDefaultDirectories(),E.createDefaultDevices(),E.createSpecialDirectories(),E.filesystems={MEMFS:JA}},init(I,C,l){E.initialized=!0,E.createStandardStreams(I,C,l)},quit(){E.initialized=!1;for(var I=0;I<E.streams.length;I++){var C=E.streams[I];C&&E.close(C)}},findObject(I,C){var l=E.analyzePath(I,C);return l.exists?l.object:null},analyzePath(I,C){try{I=(u=E.lookupPath(I,{follow:!C})).path}catch{}var l={isRoot:!1,exists:!1,error:0,name:null,path:null,object:null,parentExists:!1,parentPath:null,parentObject:null};try{var u=E.lookupPath(I,{parent:!0});l.parentExists=!0,l.parentPath=u.path,l.parentObject=u.node,l.name=wA.basename(I),u=E.lookupPath(I,{follow:!C}),l.exists=!0,l.path=u.path,l.object=u.node,l.name=u.node.name,l.isRoot=u.path==="/"}catch(w){l.error=w.errno}return l},createPath(I,C,l,u){I=typeof I=="string"?I:E.getPath(I);for(var w=C.split("/").reverse();w.length;){var R=w.pop();if(R){var v=wA.join2(I,R);try{E.mkdir(v)}catch{}I=v}}return v},createFile(I,C,l,u,w){var R=wA.join2(typeof I=="string"?I:E.getPath(I),C),v=qg(u,w);return E.create(R,v)},createDataFile(I,C,l,u,w,R){var v=C;I&&(I=typeof I=="string"?I:E.getPath(I),v=C?wA.join2(I,C):I);var N=qg(u,w),CA=E.create(v,N);if(l){if(typeof l=="string"){for(var vA=new Array(l.length),RA=0,hA=l.length;RA<hA;++RA)vA[RA]=l.charCodeAt(RA);l=vA}E.chmod(CA,146|N);var EA=E.open(CA,577);E.write(EA,l,0,l.length,0,R),E.close(EA),E.chmod(CA,N)}},createDevice(I,C,l,u){var w=wA.join2(typeof I=="string"?I:E.getPath(I),C),R=qg(!!l,!!u);E.createDevice.major??=64;var v=E.makedev(E.createDevice.major++,0);return E.registerDevice(v,{open(N){N.seekable=!1},close(N){u?.buffer?.length&&u(10)},read(N,CA,vA,RA,hA){for(var EA=0,lA=0;lA<RA;lA++){var Ee;try{Ee=l()}catch{throw new E.ErrnoError(29)}if(Ee===void 0&&EA===0)throw new E.ErrnoError(6);if(Ee==null)break;EA++,CA[vA+lA]=Ee}return EA&&(N.node.timestamp=Date.now()),EA},write(N,CA,vA,RA,hA){for(var EA=0;EA<RA;EA++)try{u(CA[vA+EA])}catch{throw new E.ErrnoError(29)}return RA&&(N.node.timestamp=Date.now()),EA}}),E.mkdev(w,R,v)},forceLoadFile(I){if(I.isDevice||I.isFolder||I.link||I.contents)return!0;if(typeof XMLHttpRequest<"u")throw new Error("Lazy loading should have been performed (contents set) in createLazyFile, but it was not. Lazy loading only works in web workers. Use --embed-file or --preload-file in emcc on the main thread.");try{I.contents=readBinary(I.url),I.usedBytes=I.contents.length}catch{throw new E.ErrnoError(29)}},createLazyFile(I,C,l,u,w){class R{constructor(){this.lengthKnown=!1,this.chunks=[]}get(hA){if(!(hA>this.length-1||hA<0)){var EA=hA%this.chunkSize,lA=hA/this.chunkSize|0;return this.getter(lA)[EA]}}setDataGetter(hA){this.getter=hA}cacheLength(){var hA=new XMLHttpRequest;if(hA.open("HEAD",l,!1),hA.send(null),!(hA.status>=200&&hA.status<300||hA.status===304))throw new Error("Couldn't load "+l+". Status: "+hA.status);var EA,lA=Number(hA.getResponseHeader("Content-length")),Ee=(EA=hA.getResponseHeader("Accept-Ranges"))&&EA==="bytes",ce=(EA=hA.getResponseHeader("Content-Encoding"))&&EA==="gzip",Xe=1048576;Ee||(Xe=lA);var Ge=this;Ge.setDataGetter(mi=>{var Sc=mi*Xe,bs=(mi+1)*Xe-1;if(bs=Math.min(bs,lA-1),Ge.chunks[mi]===void 0&&(Ge.chunks[mi]=((Nc,XI)=>{if(Nc>XI)throw new Error("invalid range ("+Nc+", "+XI+") or no bytes requested!");if(XI>lA-1)throw new Error("only "+lA+" bytes available! programmer error!");var Ht=new XMLHttpRequest;if(Ht.open("GET",l,!1),lA!==Xe&&Ht.setRequestHeader("Range","bytes="+Nc+"-"+XI),Ht.responseType="arraybuffer",Ht.overrideMimeType&&Ht.overrideMimeType("text/plain; charset=x-user-defined"),Ht.send(null),!(Ht.status>=200&&Ht.status<300||Ht.status===304))throw new Error("Couldn't load "+l+". Status: "+Ht.status);return Ht.response!==void 0?new Uint8Array(Ht.response||[]):bo(Ht.responseText||"",!0)})(Sc,bs)),Ge.chunks[mi]===void 0)throw new Error("doXHR failed!");return Ge.chunks[mi]}),!ce&&lA||(Xe=lA=1,lA=this.getter(0).length,Xe=lA,m("LazyFiles on gzip forces download of the whole file when length is accessed")),this._length=lA,this._chunkSize=Xe,this.lengthKnown=!0}get length(){return this.lengthKnown||this.cacheLength(),this._length}get chunkSize(){return this.lengthKnown||this.cacheLength(),this._chunkSize}}if(typeof XMLHttpRequest<"u"){if(!ENVIRONMENT_IS_WORKER)throw"Cannot do synchronous binary XHRs outside webworkers in modern browsers. Use --embed-file or --preload-file in emcc";var v={isDevice:!1,contents:new R}}else v={isDevice:!1,url:l};var N=E.createFile(I,C,v,u,w);v.contents?N.contents=v.contents:v.url&&(N.contents=null,N.url=v.url),Object.defineProperties(N,{usedBytes:{get:function(){return this.contents.length}}});var CA={};function vA(RA,hA,EA,lA,Ee){var ce=RA.node.contents;if(Ee>=ce.length)return 0;var Xe=Math.min(ce.length-Ee,lA);if(ce.slice)for(var Ge=0;Ge<Xe;Ge++)hA[EA+Ge]=ce[Ee+Ge];else for(Ge=0;Ge<Xe;Ge++)hA[EA+Ge]=ce.get(Ee+Ge);return Xe}return Object.keys(N.stream_ops).forEach(RA=>{var hA=N.stream_ops[RA];CA[RA]=function(){return E.forceLoadFile(N),hA(...arguments)}}),CA.read=(RA,hA,EA,lA,Ee)=>(E.forceLoadFile(N),vA(RA,hA,EA,lA,Ee)),CA.mmap=(RA,hA,EA,lA,Ee)=>{E.forceLoadFile(N);var ce=Zg(hA);if(!ce)throw new E.ErrnoError(48);return vA(RA,A,ce,hA,EA),{ptr:ce,allocated:!0}},N.stream_ops=CA,N}},oA={DEFAULT_POLLMASK:5,calculateAt(I,C,l){if(wA.isAbs(C))return C;var u;if(I===-100?u=E.cwd():u=oA.getStreamFromFD(I).path,C.length==0){if(!l)throw new E.ErrnoError(44);return u}return wA.join2(u,C)},doStat(I,C,l){var u=I(C);o[l>>2]=u.dev,o[l+4>>2]=u.mode,g[l+8>>2]=u.nlink,o[l+12>>2]=u.uid,o[l+16>>2]=u.gid,o[l+20>>2]=u.rdev,a[l+24>>3]=BigInt(u.size),o[l+32>>2]=4096,o[l+36>>2]=u.blocks;var w=u.atime.getTime(),R=u.mtime.getTime(),v=u.ctime.getTime();return a[l+40>>3]=BigInt(Math.floor(w/1e3)),g[l+48>>2]=w%1e3*1e3*1e3,a[l+56>>3]=BigInt(Math.floor(R/1e3)),g[l+64>>2]=R%1e3*1e3*1e3,a[l+72>>3]=BigInt(Math.floor(v/1e3)),g[l+80>>2]=v%1e3*1e3*1e3,a[l+88>>3]=BigInt(u.ino),0},doMsync(I,C,l,u,w){if(!E.isFile(C.node.mode))throw new E.ErrnoError(43);if(2&u)return 0;var R=n.slice(I,I+l);E.msync(C,R,w,l,u)},getStreamFromFD:I=>E.getStreamChecked(I),varargs:void 0,getStr:I=>DA(I)};function fA(){var I=o[+oA.varargs>>2];return oA.varargs+=4,I}var VA=fA,Ne=I=>I<-9007199254740992||I>9007199254740992?NaN:Number(I),tt=(I,C,l)=>ui(I,n,C,l),dt=I=>{var C=(I-Q.buffer.byteLength+65535)/65536|0;try{return Q.grow(C),M(),1}catch{}},ni={},oe=()=>{if(!oe.strings){var I={USER:"web_user",LOGNAME:"web_user",PATH:"/",PWD:"/",HOME:"/home/web_user",LANG:(typeof navigator=="object"&&navigator.languages&&navigator.languages[0]||"C").replace("-","_")+".UTF-8",_:"./this.program"};for(var C in ni)ni[C]===void 0?delete I[C]:I[C]=ni[C];var l=[];for(var C in I)l.push(`${C}=${I[C]}`);oe.strings=l}return oe.strings},zI=I=>{throw`exit(${I})`},jI=I=>ht(I);E.createPreloadedFile=(I,C,l,u,w,R,v,N,CA,vA)=>{var RA=C?we.resolve(wA.join2(I,C)):I,hA=getUniqueRunDependency(`cp ${RA}`);function EA(lA){(function(Ee){vA?.(),N||((ce,Xe,Ge,mi,Sc,bs)=>{E.createDataFile(ce,Xe,Ge,mi,Sc,bs)})(I,C,Ee,u,w,CA),R?.(),removeRunDependency(hA)})(lA)}addRunDependency(hA),typeof l=="string"?((lA,Ee,ce,Xe)=>{var Ge=Xe?"":getUniqueRunDependency(`al ${lA}`);readAsync(lA).then(mi=>{Ee(new Uint8Array(mi)),Ge&&removeRunDependency(Ge)},mi=>{if(!ce)throw`Loading data file "${lA}" failed.`;ce()}),Ge&&addRunDependency(Ge)})(l,EA,v):EA(l)},E.staticInit();var He,Oi,ht,On,ks={a:(I,C,l,u)=>{p(`Assertion failed: ${DA(I)}, at: `+[C?DA(C):"unknown filename",l,u?DA(u):"unknown function"])},b:(I,C,l)=>{throw new xA(I).init(C,l),I},v:function(I,C,l,u){try{if(C=oA.getStr(C),C=oA.calculateAt(I,C),-8&l)return-28;var w=E.lookupPath(C,{follow:!0}).node;if(!w)return-44;var R="";return 4&l&&(R+="r"),2&l&&(R+="w"),1&l&&(R+="x"),R&&E.nodePermissions(w,R)?-2:0}catch(v){if(E===void 0||v.name!=="ErrnoError")throw v;return-v.errno}},f:function(I,C,l){oA.varargs=l;try{var u=oA.getStreamFromFD(I);switch(C){case 0:if((w=fA())<0)return-28;for(;E.streams[w];)w++;return E.dupStream(u,w).fd;case 1:case 2:case 13:case 14:return 0;case 3:return u.flags;case 4:var w=fA();return u.flags|=w,0;case 12:return w=VA(),i[w+0>>1]=2,0}return-28}catch(R){if(E===void 0||R.name!=="ErrnoError")throw R;return-R.errno}},u:function(I,C){try{var l=oA.getStreamFromFD(I);return oA.doStat(E.stat,l.path,C)}catch(u){if(E===void 0||u.name!=="ErrnoError")throw u;return-u.errno}},j:function(I,C,l){oA.varargs=l;try{var u=oA.getStreamFromFD(I);switch(C){case 21509:case 21510:case 21511:case 21512:case 21524:case 21515:return u.tty?0:-59;case 21505:if(!u.tty)return-59;if(u.tty.ops.ioctl_tcgets){var w=u.tty.ops.ioctl_tcgets(u),R=VA();o[R>>2]=w.c_iflag||0,o[R+4>>2]=w.c_oflag||0,o[R+8>>2]=w.c_cflag||0,o[R+12>>2]=w.c_lflag||0;for(var v=0;v<32;v++)A[R+v+17]=w.c_cc[v]||0;return 0}return 0;case 21506:case 21507:case 21508:if(!u.tty)return-59;if(u.tty.ops.ioctl_tcsets){R=VA();var N=o[R>>2],CA=o[R+4>>2],vA=o[R+8>>2],RA=o[R+12>>2],hA=[];for(v=0;v<32;v++)hA.push(A[R+v+17]);return u.tty.ops.ioctl_tcsets(u.tty,C,{c_iflag:N,c_oflag:CA,c_cflag:vA,c_lflag:RA,c_cc:hA})}return 0;case 21519:return u.tty?(R=VA(),o[R>>2]=0,0):-59;case 21520:return u.tty?-28:-59;case 21531:return R=VA(),E.ioctl(u,C,R);case 21523:if(!u.tty)return-59;if(u.tty.ops.ioctl_tiocgwinsz){var EA=u.tty.ops.ioctl_tiocgwinsz(u.tty);R=VA(),i[R>>1]=EA[0],i[R+2>>1]=EA[1]}return 0;default:return-28}}catch(lA){if(E===void 0||lA.name!=="ErrnoError")throw lA;return-lA.errno}},s:function(I,C,l,u){try{C=oA.getStr(C);var w=256&u,R=4096&u;return u&=-6401,C=oA.calculateAt(I,C,R),oA.doStat(w?E.lstat:E.stat,C,l)}catch(v){if(E===void 0||v.name!=="ErrnoError")throw v;return-v.errno}},m:function(I,C,l,u){oA.varargs=u;try{C=oA.getStr(C),C=oA.calculateAt(I,C);var w=u?fA():0;return E.open(C,l,w).fd}catch(R){if(E===void 0||R.name!=="ErrnoError")throw R;return-R.errno}},t:function(I,C){try{return I=oA.getStr(I),oA.doStat(E.stat,I,C)}catch(l){if(E===void 0||l.name!=="ErrnoError")throw l;return-l.errno}},i:()=>{p("")},n:function(I,C,l,u,w,R,v){w=Ne(w);try{if(isNaN(w))return 61;var N=oA.getStreamFromFD(u),CA=E.mmap(N,I,w,C,l),vA=CA.ptr;return o[R>>2]=CA.allocated,g[v>>2]=vA,0}catch(RA){if(E===void 0||RA.name!=="ErrnoError")throw RA;return-RA.errno}},o:function(I,C,l,u,w,R){R=Ne(R);try{var v=oA.getStreamFromFD(w);2&l&&oA.doMsync(I,v,C,u,R)}catch(N){if(E===void 0||N.name!=="ErrnoError")throw N;return-N.errno}},k:(I,C,l,u)=>{var w=new Date().getFullYear(),R=new Date(w,0,1),v=new Date(w,6,1),N=R.getTimezoneOffset(),CA=v.getTimezoneOffset(),vA=Math.max(N,CA);g[I>>2]=60*vA,o[C>>2]=+(N!=CA);var RA=lA=>{var Ee=lA>=0?"-":"+",ce=Math.abs(lA);return`UTC${Ee}${String(Math.floor(ce/60)).padStart(2,"0")}${String(ce%60).padStart(2,"0")}`},hA=RA(N),EA=RA(CA);CA<N?(tt(hA,l,17),tt(EA,u,17)):(tt(hA,u,17),tt(EA,l,17))},h:()=>Date.now(),l:I=>{var C=n.length,l=2147483648;if((I>>>=0)>l)return!1;for(var u=1;u<=4;u*=2){var w=C*(1+.2/u);w=Math.min(w,I+100663296);var R=Math.min(l,Ti(Math.max(I,w),65536));if(dt(R))return!0}return!1},q:(I,C)=>{var l=0;return oe().forEach((u,w)=>{var R=C+l;g[I+4*w>>2]=R,((v,N)=>{for(var CA=0;CA<v.length;++CA)A[N++]=v.charCodeAt(CA);A[N]=0})(u,R),l+=u.length+1}),0},r:(I,C)=>{var l=oe();g[I>>2]=l.length;var u=0;return l.forEach(w=>u+=w.length+1),g[C>>2]=u,0},g:zI,e:function(I){try{var C=oA.getStreamFromFD(I);return E.close(C),0}catch(l){if(E===void 0||l.name!=="ErrnoError")throw l;return l.errno}},d:function(I,C,l,u){try{var w=((R,v,N,CA)=>{for(var vA=0,RA=0;RA<N;RA++){var hA=g[v>>2],EA=g[v+4>>2];v+=8;var lA=E.read(R,A,hA,EA,CA);if(lA<0)return-1;if(vA+=lA,lA<EA)break;CA!==void 0&&(CA+=lA)}return vA})(oA.getStreamFromFD(I),C,l);return g[u>>2]=w,0}catch(R){if(E===void 0||R.name!=="ErrnoError")throw R;return R.errno}},p:function(I,C,l,u){C=Ne(C);try{if(isNaN(C))return 61;var w=oA.getStreamFromFD(I);return E.llseek(w,C,l),a[u>>3]=BigInt(w.position),w.getdents&&C===0&&l===0&&(w.getdents=null),0}catch(R){if(E===void 0||R.name!=="ErrnoError")throw R;return R.errno}},c:function(I,C,l,u){try{var w=((R,v,N,CA)=>{for(var vA=0,RA=0;RA<N;RA++){var hA=g[v>>2],EA=g[v+4>>2];v+=8;var lA=E.write(R,A,hA,EA,CA);if(lA<0)return-1;if(vA+=lA,lA<EA)break;CA!==void 0&&(CA+=lA)}return vA})(oA.getStreamFromFD(I),C,l);return g[u>>2]=w,0}catch(R){if(E===void 0||R.name!=="ErrnoError")throw R;return R.errno}},w:function(I){return c.agerrMessages.push(DA(I)),0}};c.ccall=(I,C,l,u,w)=>{var R={string:EA=>{var lA=0;return EA!=null&&EA!==0&&(lA=(Ee=>{var ce=he(Ee)+1,Xe=jI(ce);return tt(Ee,Xe,ce),Xe})(EA)),lA},array:EA=>{var lA,Ee,ce=jI(EA.length);return lA=EA,Ee=ce,A.set(lA,Ee),ce}},v=(EA=>c["_"+EA])(I),N=[],CA=0;if(u)for(var vA=0;vA<u.length;vA++){var RA=R[l[vA]];RA?(CA===0&&(CA=On()),N[vA]=RA(u[vA])):N[vA]=u[vA]}var hA=v(...N);return hA=function(EA){return CA!==0&&Oi(CA),function(lA){return C==="string"?DA(lA):C==="boolean"?!!lA:lA}(EA)}(hA)},c.getValue=function(I){let C=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"i8";switch(C.endsWith("*")&&(C="*"),C){case"i1":case"i8":return A[I];case"i16":return i[I>>1];case"i32":return o[I>>2];case"i64":return a[I>>3];case"float":return r[I>>2];case"double":return s[I>>3];case"*":return g[I>>2];default:p(`invalid type for getValue: ${C}`)}},c.PATH=wA,c.UTF8ToString=DA,c.stringToUTF8=tt,c.lengthBytesUTF8=he,c.FS=E;var qv={a:ks};return WebAssembly.instantiate(c.wasm,qv).then(I=>{var C=I.instance.exports;c._viz_set_y_invert=C.z,c._viz_set_reduce=C.A,c._viz_get_graphviz_version=C.B,c._viz_get_plugin_list=C.C,c._viz_create_graph=C.D,c._viz_read_one_graph=C.E,c._viz_string_dup=C.F,c._viz_string_dup_html=C.G,c._viz_string_free=C.H,c._viz_add_node=C.I,c._viz_add_edge=C.J,c._viz_add_subgraph=C.K,c._viz_set_default_graph_attribute=C.L,c._viz_set_default_node_attribute=C.M,c._viz_set_default_edge_attribute=C.N,c._viz_set_attribute=C.O,c._viz_free_graph=C.P,c._viz_create_context=C.Q,c._viz_free_context=C.R,c._viz_layout=C.S,c._viz_free_layout=C.T,c._viz_reset_errors=C.U,c._viz_render=C.V,c._free=C.X,c._malloc=C.Y,He=C.Z,Oi=C._,ht=C.$,On=C.aa,Q=C.x,M(),function(l){l.y(),c.noFSInit||E.initialized||E.init(),E.ignorePermissions=!1}(C),t(c)}),f},$k=[[/^Error: (.*)/,"error"],[/^Warning: (.*)/,"warning"]];function Ab(t,e){let A=t.ccall("viz_get_plugin_list","number",["string"],[e]);if(A==0)throw new Error(`couldn't get plugin list: ${e}`);let i=[],o,n=A;for(;o=t.getValue(n,"*");)i.push(t.UTF8ToString(o)),t.ccall("free","number",["number"],[o]),n+=4;return t.ccall("free","number",["number"],[A]),i}function eb(t,e,A,i){let o,n,g,r;try{if(t.agerrMessages=[],t.stderrMessages=[],r=function(a,Q){return Q?Q.map(c=>{if(typeof c.name!="string")throw new Error("image name must be a string");if(typeof c.width!="number"&&typeof c.width!="string")throw new Error("image width must be a number or string");if(typeof c.height!="number"&&typeof c.height!="string")throw new Error("image height must be a number or string");let f=a.PATH.join("/",c.name),m=`<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${c.width}" height="${c.height}"></svg>
`),h(),d(4,"mat-form-field",1)(5,"input",2),Vt("ngModelChange",function(n){return si(i.newCaseId,n)||(i.newCaseId=n),n}),h()(),d(6,"mat-dialog-actions",3)(7,"button",4),k(8,"Cancel"),h(),d(9,"button",5),G("click",function(){return i.createNewEvalCase()}),k(10,"Create"),h()()),A&2&&(D(5),qt("ngModel",i.newCaseId))},dependencies:[ro,ai,jt,ho,Hn,Et,uo,mo,Do,Yn],encapsulation:2})};var bI=class t{constructor(e,A,i){this.evalService=e;this.data=A;this.dialogRef=i}newSetId="evalset"+RI().slice(0,6);createNewEvalSet(){!this.newSetId||this.newSetId==""?alert("Cannot create eval set with empty id!"):this.evalService.createNewEvalSet(this.data.appName,this.newSetId).subscribe(e=>{this.dialogRef.close(!0)})}static \u0275fac=function(A){return new(A||t)(V(po),V(ii),V(rt))};static \u0275cmp=O({type:t,selectors:[["app-new-eval-set-dialog-component"]],standalone:!1,decls:11,vars:1,consts:[["mat-dialog-title",""],[2,"padding-left","20px","padding-right","24px"],["matInput","",3,"ngModelChange","ngModel"],["align","end"],["mat-button","","mat-dialog-close",""],["mat-button","","cdkFocusInitial","",3,"click"]],template:function(A,i){A&1&&(d(0,"h2",0),k(1,"Create New Eval Set"),h(),d(2,"mat-dialog-content"),k(3,` Please enter the eval set name
`).map(n=>{let g=n.match(A.other.beginningSpace);if(g===null)return n;let[r]=g;return r.length>=o.length?n.slice(o.length):n}).join(`
`)}var fs=class{options;rules;lexer;constructor(e){this.options=e||Jg}space(e){let A=this.rules.block.newline.exec(e);if(A&&A[0].length>0)return{type:"space",raw:A[0]}}code(e){let A=this.rules.block.code.exec(e);if(A){let i=A[0].replace(this.rules.other.codeRemoveIndent,"");return{type:"code",raw:A[0],codeBlockStyle:"indented",text:this.options.pedantic?i:LI(i,`
`)}}blockquote(e){let A=this.rules.block.blockquote.exec(e);if(A){let i=LI(A[0],`
`).split(`
`),c=Q.replace(this.rules.other.blockquoteSetextReplace,`
    $1`).replace(this.rules.other.blockquoteSetextReplace2,"");o=o?`${o}
${Q}`:Q,n=n?`${n}
${c}`:c;let f=this.lexer.state.top;if(this.lexer.state.top=!0,this.lexer.blockTokens(c,g,!0),this.lexer.state.top=f,i.length===0)break;let m=g.at(-1);if(m?.type==="code")break;if(m?.type==="blockquote"){let p=m,M=p.raw+`
`+i.join(`
`),K=this.blockquote(M);g[g.length-1]=K,o=o.substring(0,o.length-p.raw.length)+K.raw,n=n.substring(0,n.length-p.text.length)+K.text;break}else if(m?.type==="list"){let p=m,M=p.raw+`
`+i.join(`
`),K=this.list(M);g[g.length-1]=K,o=o.substring(0,o.length-m.raw.length)+K.raw,n=n.substring(0,n.length-p.raw.length)+K.raw,i=M.substring(g.at(-1).raw.length).split(`
`,1)[0].replace(this.rules.other.listReplaceTabs,DA=>" ".repeat(3*DA.length)),m=e.split(`
`,e=e.substring(m.length+1),a=!0),!a){let DA=this.rules.other.nextBulletRegex(M),xA=this.rules.other.hrRegex(M),wA=this.rules.other.fencesBeginRegex(M),wt=this.rules.other.headingBeginRegex(M),we=this.rules.other.htmlBeginRegex(M);for(;e;){let Fe=e.split(`
`+m}!p&&!m.trim()&&(p=!0),Q+=Fe+`
`),this.blockTokens(e,this.tokens);for(let A=0;A<this.inlineQueue.length;A++){let i=this.inlineQueue[A];this.inlineTokens(i.src,i.tokens)}return this.inlineQueue=[],this.tokens}blockTokens(e,A=[],i=!1){for(this.options.pedantic&&(e=e.replace(pt.tabCharGlobal,"    ").replace(pt.spaceLine,""));e;){let o;if(this.options.extensions?.block?.some(g=>(o=g.call({lexer:this},e,A))?(e=e.substring(o.raw.length),A.push(o),!0):!1))continue;if(o=this.tokenizer.space(e)){e=e.substring(o.raw.length);let g=A.at(-1);o.raw.length===1&&g!==void 0?g.raw+=`
`:A.push(o);continue}if(o=this.tokenizer.code(e)){e=e.substring(o.raw.length);let g=A.at(-1);g?.type==="paragraph"||g?.type==="text"?(g.raw+=`
`+o.raw,g.text+=`
`+o.text,this.inlineQueue.at(-1).src=g.text):A.push(o);continue}if(o=this.tokenizer.fences(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.heading(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.hr(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.blockquote(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.list(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.html(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.def(e)){e=e.substring(o.raw.length);let g=A.at(-1);g?.type==="paragraph"||g?.type==="text"?(g.raw+=`
`+o.raw,g.text+=`
`+o.raw,this.inlineQueue.at(-1).src=g.text):this.tokens.links[o.tag]||(this.tokens.links[o.tag]={href:o.href,title:o.title});continue}if(o=this.tokenizer.table(e)){e=e.substring(o.raw.length),A.push(o);continue}if(o=this.tokenizer.lheading(e)){e=e.substring(o.raw.length),A.push(o);continue}let n=e;if(this.options.extensions?.startBlock){let g=1/0,r=e.slice(1),s;this.options.extensions.startBlock.forEach(a=>{s=a.call({lexer:this},r),typeof s=="number"&&s>=0&&(g=Math.min(g,s))}),g<1/0&&g>=0&&(n=e.substring(0,g+1))}if(this.state.top&&(o=this.tokenizer.paragraph(n))){let g=A.at(-1);i&&g?.type==="paragraph"?(g.raw+=`
`+o.raw,g.text+=`
`+o.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=g.text):A.push(o),i=n.length!==e.length,e=e.substring(o.raw.length);continue}if(o=this.tokenizer.text(e)){e=e.substring(o.raw.length);let g=A.at(-1);g?.type==="text"?(g.raw+=`
`+o.raw,g.text+=`
`+o.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=g.text):A.push(o);continue}if(e){let g="Infinite loop on byte: "+e.charCodeAt(0);if(this.options.silent){console.error(g);break}else throw new Error(g)}}return this.state.top=!0,A}inline(e,A=[]){return this.inlineQueue.push({src:e,tokens:A}),A}inlineTokens(e,A=[]){let i=e,o=null;if(this.tokens.links){let r=Object.keys(this.tokens.links);if(r.length>0)for(;(o=this.tokenizer.rules.inline.reflinkSearch.exec(i))!=null;)r.includes(o[0].slice(o[0].lastIndexOf("[")+1,-1))&&(i=i.slice(0,o.index)+"["+"a".repeat(o[0].length-2)+"]"+i.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex))}for(;(o=this.tokenizer.rules.inline.anyPunctuation.exec(i))!=null;)i=i.slice(0,o.index)+"++"+i.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);for(;(o=this.tokenizer.rules.inline.blockSkip.exec(i))!=null;)i=i.slice(0,o.index)+"["+"a".repeat(o[0].length-2)+"]"+i.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);let n=!1,g="";for(;e;){n||(g=""),n=!1;let r;if(this.options.extensions?.inline?.some(a=>(r=a.call({lexer:this},e,A))?(e=e.substring(r.raw.length),A.push(r),!0):!1))continue;if(r=this.tokenizer.escape(e)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.tag(e)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.link(e)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.reflink(e,this.tokens.links)){e=e.substring(r.raw.length);let a=A.at(-1);r.type==="text"&&a?.type==="text"?(a.raw+=r.raw,a.text+=r.text):A.push(r);continue}if(r=this.tokenizer.emStrong(e,i,g)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.codespan(e)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.br(e)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.del(e)){e=e.substring(r.raw.length),A.push(r);continue}if(r=this.tokenizer.autolink(e)){e=e.substring(r.raw.length),A.push(r);continue}if(!this.state.inLink&&(r=this.tokenizer.url(e))){e=e.substring(r.raw.length),A.push(r);continue}let s=e;if(this.options.extensions?.startInline){let a=1/0,Q=e.slice(1),c;this.options.extensions.startInline.forEach(f=>{c=f.call({lexer:this},Q),typeof c=="number"&&c>=0&&(a=Math.min(a,c))}),a<1/0&&a>=0&&(s=e.substring(0,a+1))}if(r=this.tokenizer.inlineText(s)){e=e.substring(r.raw.length),r.raw.slice(-1)!=="_"&&(g=r.raw.slice(-1)),n=!0;let a=A.at(-1);a?.type==="text"?(a.raw+=r.raw,a.text+=r.text):A.push(r);continue}if(e){let a="Infinite loop on byte: "+e.charCodeAt(0);if(this.options.silent){console.error(a);break}else throw new Error(a)}}return A}},Ro=class{options;parser;constructor(e){this.options=e||Jg}space(e){return""}code({text:e,lang:A,escaped:i}){let o=(A||"").match(pt.notSpaceStart)?.[0],n=e.replace(pt.endingNewline,"")+`
`;return o?'<pre><code class="language-'+Mo(o)+'">'+(i?n:Mo(n,!0))+`</code></pre>
`:"<pre><code>"+(i?n:Mo(n,!0))+`</code></pre>
`}blockquote({tokens:e}){return`<blockquote>
${this.parser.parse(e)}</blockquote>
`}html({text:e}){return e}heading({tokens:e,depth:A}){return`<h${A}>${this.parser.parseInline(e)}</h${A}>
`}hr(e){return`<hr>
`}list(e){let A=e.ordered,i=e.start,o="";for(let r=0;r<e.items.length;r++){let s=e.items[r];o+=this.listitem(s)}let n=A?"ol":"ul",g=A&&i!==1?' start="'+i+'"':"";return"<"+n+g+`>
`+o+"</"+n+`>
`}listitem(e){let A="";if(e.task){let i=this.checkbox({checked:!!e.checked});e.loose?e.tokens[0]?.type==="paragraph"?(e.tokens[0].text=i+" "+e.tokens[0].text,e.tokens[0].tokens&&e.tokens[0].tokens.length>0&&e.tokens[0].tokens[0].type==="text"&&(e.tokens[0].tokens[0].text=i+" "+Mo(e.tokens[0].tokens[0].text),e.tokens[0].tokens[0].escaped=!0)):e.tokens.unshift({type:"text",raw:i+" ",text:i+" ",escaped:!0}):A+=i+" "}return A+=this.parser.parse(e.tokens,!!e.loose),`<li>${A}</li>
`}checkbox({checked:e}){return"<input "+(e?'checked="" ':"")+'disabled="" type="checkbox">'}paragraph({tokens:e}){return`<p>${this.parser.parseInline(e)}</p>
`}table(e){let A="",i="";for(let n=0;n<e.header.length;n++)i+=this.tablecell(e.header[n]);A+=this.tablerow({text:i});let o="";for(let n=0;n<e.rows.length;n++){let g=e.rows[n];i="";for(let r=0;r<g.length;r++)i+=this.tablecell(g[r]);o+=this.tablerow({text:i})}return o&&(o=`<tbody>${o}</tbody>`),`<table>
<thead>
`+A+`</thead>
`+o+`</table>
`}tablerow({text:e}){return`<tr>
${e}</tr>
`}tablecell(e){let A=this.parser.parseInline(e.tokens),i=e.header?"th":"td";return(e.align?`<${i} align="${e.align}">`:`<${i}>`)+A+`</${i}>
`}strong({tokens:e}){return`<strong>${this.parser.parseInline(e)}</strong>`}em({tokens:e}){return`<em>${this.parser.parseInline(e)}</em>`}codespan({text:e}){return`<code>${Mo(e,!0)}</code>`}br(e){return"<br>"}del({tokens:e}){return`<del>${this.parser.parseInline(e)}</del>`}link({href:e,title:A,tokens:i}){let o=this.parser.parseInline(i),n=MF(e);if(n===null)return o;e=n;let g='<a href="'+e+'"';return A&&(g+=' title="'+Mo(A)+'"'),g+=">"+o+"</a>",g}image({href:e,title:A,text:i,tokens:o}){o&&(i=this.parser.parseInline(o,this.parser.textRenderer));let n=MF(e);if(n===null)return Mo(i);e=n;let g=`<img src="${e}" alt="${i}"`;return A&&(g+=` title="${Mo(A)}"`),g+=">",g}text(e){return"tokens"in e&&e.tokens?this.parser.parseInline(e.tokens):"escaped"in e&&e.escaped?e.text:Mo(e.text)}},KI=class{strong({text:e}){return e}em({text:e}){return e}codespan({text:e}){return e}del({text:e}){return e}html({text:e}){return e}text({text:e}){return e}link({text:e}){return""+e}image({text:e}){return""+e}br(){return""}},xi=class t{options;renderer;textRenderer;constructor(e){this.options=e||Jg,this.options.renderer=this.options.renderer||new Ro,this.renderer=this.options.renderer,this.renderer.options=this.options,this.renderer.parser=this,this.textRenderer=new KI}static parse(e,A){return new t(A).parse(e)}static parseInline(e,A){return new t(A).parseInline(e)}parse(e,A=!0){let i="";for(let o=0;o<e.length;o++){let n=e[o];if(this.options.extensions?.renderers?.[n.type]){let r=n,s=this.options.extensions.renderers[r.type].call({parser:this},r);if(s!==!1||!["space","hr","heading","code","table","blockquote","list","html","paragraph","text"].includes(r.type)){i+=s||"";continue}}let g=n;switch(g.type){case"space":{i+=this.renderer.space(g);continue}case"hr":{i+=this.renderer.hr(g);continue}case"heading":{i+=this.renderer.heading(g);continue}case"code":{i+=this.renderer.code(g);continue}case"table":{i+=this.renderer.table(g);continue}case"blockquote":{i+=this.renderer.blockquote(g);continue}case"list":{i+=this.renderer.list(g);continue}case"html":{i+=this.renderer.html(g);continue}case"paragraph":{i+=this.renderer.paragraph(g);continue}case"text":{let r=g,s=this.renderer.text(r);for(;o+1<e.length&&e[o+1].type==="text";)r=e[++o],s+=`
`+this.renderer.text(r);A?i+=this.renderer.paragraph({type:"paragraph",raw:s,text:s,tokens:[{type:"text",raw:s,text:s,escaped:!0}]}):i+=s;continue}default:{let r='Token with "'+g.type+'" type was not found.';if(this.options.silent)return console.error(r),"";throw new Error(r)}}}return i}parseInline(e,A=this.renderer){let i="";for(let o=0;o<e.length;o++){let n=e[o];if(this.options.extensions?.renderers?.[n.type]){let r=this.options.extensions.renderers[n.type].call({parser:this},n);if(r!==!1||!["escape","html","link","image","strong","em","codespan","br","del","text"].includes(n.type)){i+=r||"";continue}}let g=n;switch(g.type){case"escape":{i+=A.text(g);break}case"html":{i+=A.html(g);break}case"link":{i+=A.link(g);break}case"image":{i+=A.image(g);break}case"strong":{i+=A.strong(g);break}case"em":{i+=A.em(g);break}case"codespan":{i+=A.codespan(g);break}case"br":{i+=A.br(g);break}case"del":{i+=A.del(g);break}case"text":{i+=A.text(g);break}default:{let r='Token with "'+g.type+'" type was not found.';if(this.options.silent)return console.error(r),"";throw new Error(r)}}}return i}},Ds=class{options;block;constructor(e){this.options=e||Jg}static passThroughHooks=new Set(["preprocess","postprocess","processAllTokens"]);preprocess(e){return e}postprocess(e){return e}processAllTokens(e){return e}provideLexer(){return this.block?Ui.lex:Ui.lexInline}provideParser(){return this.block?xi.parse:xi.parseInline}},mD=class{defaults=DD();options=this.setOptions;parse=this.parseMarkdown(!0);parseInline=this.parseMarkdown(!1);Parser=xi;Renderer=Ro;TextRenderer=KI;Lexer=Ui;Tokenizer=fs;Hooks=Ds;constructor(...e){this.use(...e)}walkTokens(e,A){let i=[];for(let o of e)switch(i=i.concat(A.call(this,o)),o.type){case"table":{let n=o;for(let g of n.header)i=i.concat(this.walkTokens(g.tokens,A));for(let g of n.rows)for(let r of g)i=i.concat(this.walkTokens(r.tokens,A));break}case"list":{let n=o;i=i.concat(this.walkTokens(n.items,A));break}default:{let n=o;this.defaults.extensions?.childTokens?.[n.type]?this.defaults.extensions.childTokens[n.type].forEach(g=>{let r=n[g].flat(1/0);i=i.concat(this.walkTokens(r,A))}):n.tokens&&(i=i.concat(this.walkTokens(n.tokens,A)))}}return i}use(...e){let A=this.defaults.extensions||{renderers:{},childTokens:{}};return e.forEach(i=>{let o=b({},i);if(o.async=this.defaults.async||o.async||!1,i.extensions&&(i.extensions.forEach(n=>{if(!n.name)throw new Error("extension name required");if("renderer"in n){let g=A.renderers[n.name];g?A.renderers[n.name]=function(...r){let s=n.renderer.apply(this,r);return s===!1&&(s=g.apply(this,r)),s}:A.renderers[n.name]=n.renderer}if("tokenizer"in n){if(!n.level||n.level!=="block"&&n.level!=="inline")throw new Error("extension level must be 'block' or 'inline'");let g=A[n.level];g?g.unshift(n.tokenizer):A[n.level]=[n.tokenizer],n.start&&(n.level==="block"?A.startBlock?A.startBlock.push(n.start):A.startBlock=[n.start]:n.level==="inline"&&(A.startInline?A.startInline.push(n.start):A.startInline=[n.start]))}"childTokens"in n&&n.childTokens&&(A.childTokens[n.name]=n.childTokens)}),o.extensions=A),i.renderer){let n=this.defaults.renderer||new Ro(this.defaults);for(let g in i.renderer){if(!(g in n))throw new Error(`renderer '${g}' does not exist`);if(["options","parser"].includes(g))continue;let r=g,s=i.renderer[r],a=n[r];n[r]=(...Q)=>{let c=s.apply(n,Q);return c===!1&&(c=a.apply(n,Q)),c||""}}o.renderer=n}if(i.tokenizer){let n=this.defaults.tokenizer||new fs(this.defaults);for(let g in i.tokenizer){if(!(g in n))throw new Error(`tokenizer '${g}' does not exist`);if(["options","rules","lexer"].includes(g))continue;let r=g,s=i.tokenizer[r],a=n[r];n[r]=(...Q)=>{let c=s.apply(n,Q);return c===!1&&(c=a.apply(n,Q)),c}}o.tokenizer=n}if(i.hooks){let n=this.defaults.hooks||new Ds;for(let g in i.hooks){if(!(g in n))throw new Error(`hook '${g}' does not exist`);if(["options","block"].includes(g))continue;let r=g,s=i.hooks[r],a=n[r];Ds.passThroughHooks.has(g)?n[r]=Q=>{if(this.defaults.async)return Promise.resolve(s.call(n,Q)).then(f=>a.call(n,f));let c=s.call(n,Q);return a.call(n,c)}:n[r]=(...Q)=>{let c=s.apply(n,Q);return c===!1&&(c=a.apply(n,Q)),c}}o.hooks=n}if(i.walkTokens){let n=this.defaults.walkTokens,g=i.walkTokens;o.walkTokens=function(r){let s=[];return s.push(g.call(this,r)),n&&(s=s.concat(n.call(this,r))),s}}this.defaults=b(b({},this.defaults),o)}),this}setOptions(e){return this.defaults=b(b({},this.defaults),e),this}lexer(e,A){return Ui.lex(e,A??this.defaults)}parser(e,A){return xi.parse(e,A??this.defaults)}parseMarkdown(e){return(i,o)=>{let n=b({},o),g=b(b({},this.defaults),n),r=this.onError(!!g.silent,!!g.async);if(this.defaults.async===!0&&n.async===!1)return r(new Error("marked(): The async option was set to true by an extension. Remove async: false from the parse options object to return a Promise."));if(typeof i>"u"||i===null)return r(new Error("marked(): input parameter is undefined or null"));if(typeof i!="string")return r(new Error("marked(): input parameter is of type "+Object.prototype.toString.call(i)+", string expected"));g.hooks&&(g.hooks.options=g,g.hooks.block=e);let s=g.hooks?g.hooks.provideLexer():e?Ui.lex:Ui.lexInline,a=g.hooks?g.hooks.provideParser():e?xi.parse:xi.parseInline;if(g.async)return Promise.resolve(g.hooks?g.hooks.preprocess(i):i).then(Q=>s(Q,g)).then(Q=>g.hooks?g.hooks.processAllTokens(Q):Q).then(Q=>g.walkTokens?Promise.all(this.walkTokens(Q,g.walkTokens)).then(()=>Q):Q).then(Q=>a(Q,g)).then(Q=>g.hooks?g.hooks.postprocess(Q):Q).catch(r);try{g.hooks&&(i=g.hooks.preprocess(i));let Q=s(i,g);g.hooks&&(Q=g.hooks.processAllTokens(Q)),g.walkTokens&&this.walkTokens(Q,g.walkTokens);let c=a(Q,g);return g.hooks&&(c=g.hooks.postprocess(c)),c}catch(Q){return r(Q)}}}onError(e,A){return i=>{if(i.message+=`
`+i+"\n```":i}parseMarked(A,i,o=!1){if(i.renderer){let n=b({},i.renderer);delete n.\u0275NgxMarkdownRendererExtendedForExtensions,delete n.\u0275NgxMarkdownRendererExtendedForMermaid,delete i.renderer,ee.use({renderer:n})}return o?ee.parseInline(A,i):ee.parse(A,i)}parseEmoji(A){if(!go(this.platform))return A;if(typeof joypixels>"u"||typeof joypixels.shortnameToUnicode>"u")throw new Error(oZ);return joypixels.shortnameToUnicode(A)}renderKatex(A,i){if(go(this.platform)){if(typeof katex>"u"||typeof renderMathInElement>"u")throw new Error(nZ);renderMathInElement(A,i)}}renderClipboard(A,i,o){if(!go(this.platform))return;if(typeof ClipboardJS>"u")throw new Error(rZ);if(!i)throw new Error(sZ);let{buttonComponent:n,buttonTemplate:g}=o,r=A.querySelectorAll("pre");for(let s=0;s<r.length;s++){let a=r.item(s),Q=document.createElement("div");Q.style.position="relative",a.parentNode.insertBefore(Q,a),Q.appendChild(a);let c=document.createElement("div");c.classList.add("markdown-clipboard-toolbar"),c.style.position="absolute",c.style.top=".5em",c.style.right=".5em",c.style.zIndex="1",Q.insertAdjacentElement("beforeend",c),Q.onmouseenter=()=>c.classList.add("hover"),Q.onmouseleave=()=>c.classList.remove("hover");let f;if(n){let p=i.createComponent(n);f=p.hostView,p.changeDetectorRef.markForCheck()}else if(g)f=i.createEmbeddedView(g);else{let p=i.createComponent(AZ);f=p.hostView,p.changeDetectorRef.markForCheck()}let m;f.rootNodes.forEach(p=>{c.appendChild(p),m=new ClipboardJS(p,{text:()=>a.innerText})}),f.onDestroy(()=>m.destroy())}}renderMermaid(A,i=this.DEFAULT_MERMAID_OPTIONS){if(!go(this.platform))return;if(typeof mermaid>"u"||typeof mermaid.initialize>"u")throw new Error(gZ);let o=A.querySelectorAll(".mermaid");o.length!==0&&(mermaid.initialize(i),mermaid.run({nodes:o}))}trimIndentation(A){if(!A)return"";let i;return A.split(`
`).map(o=>{let n=i;return o.length>0&&(n=isNaN(n)?o.search(/\S|$/):Math.min(o.search(/\S|$/),n)),isNaN(i)&&(i=n),n?o.substring(n):o}).join(`
`)}static{this.\u0275fac=function(i){return new(i||t)(Z(eZ,8),Z(YF,8),Z(tZ,8),Z(iZ,8),Z(ri),Z(JF),Z(Qt,8),Z(Vo))}}static{this.\u0275prov=S({token:t,factory:t.\u0275fac})}}return t})(),TF=(()=>{class t{get disableSanitizer(){return this._disableSanitizer}set disableSanitizer(A){this._disableSanitizer=this.coerceBooleanProperty(A)}get inline(){return this._inline}set inline(A){this._inline=this.coerceBooleanProperty(A)}get clipboard(){return this._clipboard}set clipboard(A){this._clipboard=this.coerceBooleanProperty(A)}get emoji(){return this._emoji}set emoji(A){this._emoji=this.coerceBooleanProperty(A)}get katex(){return this._katex}set katex(A){this._katex=this.coerceBooleanProperty(A)}get mermaid(){return this._mermaid}set mermaid(A){this._mermaid=this.coerceBooleanProperty(A)}get lineHighlight(){return this._lineHighlight}set lineHighlight(A){this._lineHighlight=this.coerceBooleanProperty(A)}get lineNumbers(){return this._lineNumbers}set lineNumbers(A){this._lineNumbers=this.coerceBooleanProperty(A)}get commandLine(){return this._commandLine}set commandLine(A){this._commandLine=this.coerceBooleanProperty(A)}constructor(A,i,o){this.element=A,this.markdownService=i,this.viewContainerRef=o,this.error=new z,this.load=new z,this.ready=new z,this._clipboard=!1,this._commandLine=!1,this._disableSanitizer=!1,this._emoji=!1,this._inline=!1,this._katex=!1,this._lineHighlight=!1,this._lineNumbers=!1,this._mermaid=!1,this.destroyed$=new U}ngOnChanges(){this.loadContent()}loadContent(){if(this.data!=null){this.handleData();return}if(this.src!=null){this.handleSrc();return}}ngAfterViewInit(){!this.data&&!this.src&&this.handleTransclusion(),this.markdownService.reload$.pipe(pA(this.destroyed$)).subscribe(()=>this.loadContent())}ngOnDestroy(){this.destroyed$.next(),this.destroyed$.complete()}render(A,i=!1){return $e(this,null,function*(){let o={decodeHtml:i,inline:this.inline,emoji:this.emoji,mermaid:this.mermaid,disableSanitizer:this.disableSanitizer},n={clipboard:this.clipboard,clipboardOptions:this.getClipboardOptions(),katex:this.katex,katexOptions:this.katexOptions,mermaid:this.mermaid,mermaidOptions:this.mermaidOptions},g=yield this.markdownService.parse(A,o);this.element.nativeElement.innerHTML=g,this.handlePlugins(),this.markdownService.render(this.element.nativeElement,n,this.viewContainerRef),this.ready.emit()})}coerceBooleanProperty(A){return A!=null&&`${String(A)}`!="false"}getClipboardOptions(){if(this.clipboardButtonComponent||this.clipboardButtonTemplate)return{buttonComponent:this.clipboardButtonComponent,buttonTemplate:this.clipboardButtonTemplate}}handleData(){this.render(this.data)}handleSrc(){this.markdownService.getSource(this.src).subscribe({next:A=>{this.render(A).then(()=>{this.load.emit(A)})},error:A=>this.error.emit(A)})}handleTransclusion(){this.render(this.element.nativeElement.innerHTML,!0)}handlePlugins(){this.commandLine&&(this.setPluginClass(this.element.nativeElement,bD.CommandLine),this.setPluginOptions(this.element.nativeElement,{dataFilterOutput:this.filterOutput,dataHost:this.host,dataPrompt:this.prompt,dataOutput:this.output,dataUser:this.user})),this.lineHighlight&&this.setPluginOptions(this.element.nativeElement,{dataLine:this.line,dataLineOffset:this.lineOffset}),this.lineNumbers&&(this.setPluginClass(this.element.nativeElement,bD.LineNumbers),this.setPluginOptions(this.element.nativeElement,{dataStart:this.start}))}setPluginClass(A,i){let o=A.querySelectorAll("pre");for(let n=0;n<o.length;n++){let g=i instanceof Array?i:[i];o.item(n).classList.add(...g)}}setPluginOptions(A,i){let o=A.querySelectorAll("pre");for(let n=0;n<o.length;n++)Object.keys(i).forEach(g=>{let r=i[g];if(r){let s=this.toLispCase(g);o.item(n).setAttribute(s,r.toString())}})}toLispCase(A){let i=A.match(/([A-Z])/g);if(!i)return A;let o=A.toString();for(let n=0,g=i.length;n<g;n++)o=o.replace(new RegExp(i[n]),"-"+i[n].toLowerCase());return o.slice(0,1)==="-"&&(o=o.slice(1)),o}static{this.\u0275fac=function(i){return new(i||t)(V(q),V(HF),V(Qe))}}static{this.\u0275cmp=O({type:t,selectors:[["markdown"],["","markdown",""]],inputs:{data:"data",src:"src",disableSanitizer:"disableSanitizer",inline:"inline",clipboard:"clipboard",clipboardButtonComponent:"clipboardButtonComponent",clipboardButtonTemplate:"clipboardButtonTemplate",emoji:"emoji",katex:"katex",katexOptions:"katexOptions",mermaid:"mermaid",mermaidOptions:"mermaidOptions",lineHighlight:"lineHighlight",line:"line",lineOffset:"lineOffset",lineNumbers:"lineNumbers",start:"start",commandLine:"commandLine",filterOutput:"filterOutput",host:"host",prompt:"prompt",output:"output",user:"user"},outputs:{error:"error",load:"load",ready:"ready"},features:[TA],ngContentSelectors:j1,decls:1,vars:0,template:function(i,o){i&1&&(OA(),IA(0))},encapsulation:2})}}return t})();function IZ(t){return[HF,t?.loader??[],t?.clipboardOptions??[],t?.markedOptions??[],t?.mermaidOptions??[],BZ(t?.markedExtensions)??[],{provide:JF,useValue:t?.sanitize??et.HTML}]}function CZ(t){return t!=null&&t.provide!=null}function BZ(t){if(t)return t.reduce((e,A)=>{let i=CZ(A)?uA(b({},A),{multi:!0}):{provide:YF,useValue:A,multi:!0};return[...e,i]},[])}var OF=(()=>{class t{static forRoot(A){return{ngModule:t,providers:[IZ(A)]}}static forChild(){return{ngModule:t}}static{this.\u0275fac=function(i){return new(i||t)}}static{this.\u0275mod=X({type:t})}static{this.\u0275inj=j({imports:[Zo]})}}return t})();var EZ=["switch"],cZ=["*"];function lZ(t,e){t&1&&(d(0,"span",10),At(),d(1,"svg",12),P(2,"path",13),h(),d(3,"svg",14),P(4,"path",15),h()())}var dZ=new F("mat-slide-toggle-default-options",{providedIn:"root",factory:()=>({disableToggleValue:!1,hideIcon:!1,disabledInteractive:!1})}),hZ={provide:Wo,useExisting:ot(()=>ac),multi:!0},sc=class{source;checked;constructor(e,A){this.source=e,this.checked=A}},ac=(()=>{class t{_elementRef=B(q);_focusMonitor=B(Kt);_changeDetectorRef=B(KA);defaults=B(dZ);_onChange=A=>{};_onTouched=()=>{};_validatorOnChange=()=>{};_uniqueId;_checked=!1;_createChangeEvent(A){return new sc(this,A)}_labelId;get buttonId(){return`${this.id||this._uniqueId}-button`}_switchElement;focus(){this._switchElement.nativeElement.focus()}_noopAnimations;_focused;name=null;id;labelPosition="after";ariaLabel=null;ariaLabelledby=null;ariaDescribedby;required;color;disabled=!1;disableRipple=!1;tabIndex=0;get checked(){return this._checked}set checked(A){this._checked=A,this._changeDetectorRef.markForCheck()}hideIcon;disabledInteractive;change=new z;toggleChange=new z;get inputId(){return`${this.id||this._uniqueId}-input`}constructor(){B(ke).load(Ut);let A=B(new Ct("tabindex"),{optional:!0}),i=this.defaults,o=B(Ae,{optional:!0});this.tabIndex=A==null?0:parseInt(A)||0,this.color=i.color||"accent",this._noopAnimations=o==="NoopAnimations",this.id=this._uniqueId=B(re).getId("mat-mdc-slide-toggle-"),this.hideIcon=i.hideIcon??!1,this.disabledInteractive=i.disabledInteractive??!1,this._labelId=this._uniqueId+"-label"}ngAfterContentInit(){this._focusMonitor.monitor(this._elementRef,!0).subscribe(A=>{A==="keyboard"||A==="program"?(this._focused=!0,this._changeDetectorRef.markForCheck()):A||Promise.resolve().then(()=>{this._focused=!1,this._onTouched(),this._changeDetectorRef.markForCheck()})})}ngOnChanges(A){A.required&&this._validatorOnChange()}ngOnDestroy(){this._focusMonitor.stopMonitoring(this._elementRef)}writeValue(A){this.checked=!!A}registerOnChange(A){this._onChange=A}registerOnTouched(A){this._onTouched=A}validate(A){return this.required&&A.value!==!0?{required:!0}:null}registerOnValidatorChange(A){this._validatorOnChange=A}setDisabledState(A){this.disabled=A,this._changeDetectorRef.markForCheck()}toggle(){this.checked=!this.checked,this._onChange(this.checked)}_emitChangeEvent(){this._onChange(this.checked),this.change.emit(this._createChangeEvent(this.checked))}_handleClick(){this.disabled||(this.toggleChange.emit(),this.defaults.disableToggleValue||(this.checked=!this.checked,this._onChange(this.checked),this.change.emit(new sc(this,this.checked))))}_getAriaLabelledBy(){return this.ariaLabelledby?this.ariaLabelledby:this.ariaLabel?null:this._labelId}static \u0275fac=function(i){return new(i||t)};static \u0275cmp=O({type:t,selectors:[["mat-slide-toggle"]],viewQuery:function(i,o){if(i&1&&QA(EZ,5),i&2){let n;$(n=AA())&&(o._switchElement=n.first)}},hostAttrs:[1,"mat-mdc-slide-toggle"],hostVars:13,hostBindings:function(i,o){i&2&&(Dt("id",o.id),aA("tabindex",null)("aria-label",null)("name",null)("aria-labelledby",null),Je(o.color?"mat-"+o.color:""),nA("mat-mdc-slide-toggle-focused",o._focused)("mat-mdc-slide-toggle-checked",o.checked)("_mat-animation-noopable",o._noopAnimations))},inputs:{name:"name",id:"id",labelPosition:"labelPosition",ariaLabel:[0,"aria-label","ariaLabel"],ariaLabelledby:[0,"aria-labelledby","ariaLabelledby"],ariaDescribedby:[0,"aria-describedby","ariaDescribedby"],required:[2,"required","required",eA],color:"color",disabled:[2,"disabled","disabled",eA],disableRipple:[2,"disableRipple","disableRipple",eA],tabIndex:[2,"tabIndex","tabIndex",A=>A==null?0:de(A)],checked:[2,"checked","checked",eA],hideIcon:[2,"hideIcon","hideIcon",eA],disabledInteractive:[2,"disabledInteractive","disabledInteractive",eA]},outputs:{change:"change",toggleChange:"toggleChange"},exportAs:["matSlideToggle"],features:[FA([hZ,{provide:Rn,useExisting:t,multi:!0}]),TA],ngContentSelectors:cZ,decls:13,vars:27,consts:[["switch",""],["mat-internal-form-field","",3,"labelPosition"],["role","switch","type","button",1,"mdc-switch",3,"click","tabIndex","disabled"],[1,"mdc-switch__track"],[1,"mdc-switch__handle-track"],[1,"mdc-switch__handle"],[1,"mdc-switch__shadow"],[1,"mdc-elevation-overlay"],[1,"mdc-switch__ripple"],["mat-ripple","",1,"mat-mdc-slide-toggle-ripple","mat-focus-indicator",3,"matRippleTrigger","matRippleDisabled","matRippleCentered"],[1,"mdc-switch__icons"],[1,"mdc-label",3,"click","for"],["viewBox","0 0 24 24","aria-hidden","true",1,"mdc-switch__icon","mdc-switch__icon--on"],["d","M19.69,5.23L8.96,15.96l-4.23-4.23L2.96,13.5l6,6L21.46,7L19.69,5.23z"],["viewBox","0 0 24 24","aria-hidden","true",1,"mdc-switch__icon","mdc-switch__icon--off"],["d","M20 13H4v-2h16v2z"]],template:function(i,o){if(i&1){let n=rA();OA(),d(0,"div",1)(1,"button",2,0),G("click",function(){return Y(n),J(o._handleClick())}),P(3,"span",3),d(4,"span",4)(5,"span",5)(6,"span",6),P(7,"span",7),h(),d(8,"span",8),P(9,"span",9),h(),x(10,lZ,5,0,"span",10),h()()(),d(11,"label",11),G("click",function(r){return Y(n),J(r.stopPropagation())}),IA(12),h()()}if(i&2){let n=_e(2);L("labelPosition",o.labelPosition),D(),nA("mdc-switch--selected",o.checked)("mdc-switch--unselected",!o.checked)("mdc-switch--checked",o.checked)("mdc-switch--disabled",o.disabled)("mat-mdc-slide-toggle-disabled-interactive",o.disabledInteractive),L("tabIndex",o.disabled&&!o.disabledInteractive?-1:o.tabIndex)("disabled",o.disabled&&!o.disabledInteractive),aA("id",o.buttonId)("name",o.name)("aria-label",o.ariaLabel)("aria-labelledby",o._getAriaLabelledBy())("aria-describedby",o.ariaDescribedby)("aria-required",o.required||null)("aria-checked",o.checked)("aria-disabled",o.disabled&&o.disabledInteractive?"true":null),D(8),L("matRippleTrigger",n)("matRippleDisabled",o.disableRipple||o.disabled)("matRippleCentered",!0),D(),_(o.hideIcon?-1:10),D(),L("for",o.buttonId),aA("id",o._labelId)}},dependencies:[Eo,wE],styles:['.mdc-switch{align-items:center;background:none;border:none;cursor:pointer;display:inline-flex;flex-shrink:0;margin:0;outline:none;overflow:visible;padding:0;position:relative;width:var(--mdc-switch-track-width, 52px)}.mdc-switch.mdc-switch--disabled{cursor:default;pointer-events:none}.mdc-switch.mat-mdc-slide-toggle-disabled-interactive{pointer-events:auto}.mdc-switch__track{overflow:hidden;position:relative;width:100%;height:var(--mdc-switch-track-height, 32px);border-radius:var(--mdc-switch-track-shape, var(--mat-sys-corner-full))}.mdc-switch--disabled.mdc-switch .mdc-switch__track{opacity:var(--mdc-switch-disabled-track-opacity, 0.12)}.mdc-switch__track::before,.mdc-switch__track::after{border:1px solid rgba(0,0,0,0);border-radius:inherit;box-sizing:border-box;content:"";height:100%;left:0;position:absolute;width:100%;border-width:var(--mat-switch-track-outline-width, 2px);border-color:var(--mat-switch-track-outline-color, var(--mat-sys-outline))}.mdc-switch--selected .mdc-switch__track::before,.mdc-switch--selected .mdc-switch__track::after{border-width:var(--mat-switch-selected-track-outline-width, 2px);border-color:var(--mat-switch-selected-track-outline-color, transparent)}.mdc-switch--disabled .mdc-switch__track::before,.mdc-switch--disabled .mdc-switch__track::after{border-width:var(--mat-switch-disabled-unselected-track-outline-width, 2px);border-color:var(--mat-switch-disabled-unselected-track-outline-color, var(--mat-sys-on-surface))}@media(forced-colors: active){.mdc-switch__track{border-color:currentColor}}.mdc-switch__track::before{transition:transform 75ms 0ms cubic-bezier(0, 0, 0.2, 1);transform:translateX(0);background:var(--mdc-switch-unselected-track-color, var(--mat-sys-surface-variant))}.mdc-switch--selected .mdc-switch__track::before{transition:transform 75ms 0ms cubic-bezier(0.4, 0, 0.6, 1);transform:translateX(100%)}[dir=rtl] .mdc-switch--selected .mdc-switch--selected .mdc-switch__track::before{transform:translateX(-100%)}.mdc-switch--selected .mdc-switch__track::before{opacity:var(--mat-switch-hidden-track-opacity, 0);transition:var(--mat-switch-hidden-track-transition, opacity 75ms)}.mdc-switch--unselected .mdc-switch__track::before{opacity:var(--mat-switch-visible-track-opacity, 1);transition:var(--mat-switch-visible-track-transition, opacity 75ms)}.mdc-switch:enabled:hover:not(:focus):not(:active) .mdc-switch__track::before{background:var(--mdc-switch-unselected-hover-track-color, var(--mat-sys-surface-variant))}.mdc-switch:enabled:focus:not(:active) .mdc-switch__track::before{background:var(--mdc-switch-unselected-focus-track-color, var(--mat-sys-surface-variant))}.mdc-switch:enabled:active .mdc-switch__track::before{background:var(--mdc-switch-unselected-pressed-track-color, var(--mat-sys-surface-variant))}.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:hover:not(:focus):not(:active) .mdc-switch__track::before,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:focus:not(:active) .mdc-switch__track::before,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:active .mdc-switch__track::before,.mdc-switch.mdc-switch--disabled .mdc-switch__track::before{background:var(--mdc-switch-disabled-unselected-track-color, var(--mat-sys-surface-variant))}.mdc-switch__track::after{transform:translateX(-100%);background:var(--mdc-switch-selected-track-color, var(--mat-sys-primary))}[dir=rtl] .mdc-switch__track::after{transform:translateX(100%)}.mdc-switch--selected .mdc-switch__track::after{transform:translateX(0)}.mdc-switch--selected .mdc-switch__track::after{opacity:var(--mat-switch-visible-track-opacity, 1);transition:var(--mat-switch-visible-track-transition, opacity 75ms)}.mdc-switch--unselected .mdc-switch__track::after{opacity:var(--mat-switch-hidden-track-opacity, 0);transition:var(--mat-switch-hidden-track-transition, opacity 75ms)}.mdc-switch:enabled:hover:not(:focus):not(:active) .mdc-switch__track::after{background:var(--mdc-switch-selected-hover-track-color, var(--mat-sys-primary))}.mdc-switch:enabled:focus:not(:active) .mdc-switch__track::after{background:var(--mdc-switch-selected-focus-track-color, var(--mat-sys-primary))}.mdc-switch:enabled:active .mdc-switch__track::after{background:var(--mdc-switch-selected-pressed-track-color, var(--mat-sys-primary))}.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:hover:not(:focus):not(:active) .mdc-switch__track::after,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:focus:not(:active) .mdc-switch__track::after,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:active .mdc-switch__track::after,.mdc-switch.mdc-switch--disabled .mdc-switch__track::after{background:var(--mdc-switch-disabled-selected-track-color, var(--mat-sys-on-surface))}.mdc-switch__handle-track{height:100%;pointer-events:none;position:absolute;top:0;transition:transform 75ms 0ms cubic-bezier(0.4, 0, 0.2, 1);left:0;right:auto;transform:translateX(0);width:calc(100% - var(--mdc-switch-handle-width))}[dir=rtl] .mdc-switch__handle-track{left:auto;right:0}.mdc-switch--selected .mdc-switch__handle-track{transform:translateX(100%)}[dir=rtl] .mdc-switch--selected .mdc-switch__handle-track{transform:translateX(-100%)}.mdc-switch__handle{display:flex;pointer-events:auto;position:absolute;top:50%;transform:translateY(-50%);left:0;right:auto;transition:width 75ms cubic-bezier(0.4, 0, 0.2, 1),height 75ms cubic-bezier(0.4, 0, 0.2, 1),margin 75ms cubic-bezier(0.4, 0, 0.2, 1);width:var(--mdc-switch-handle-width);height:var(--mdc-switch-handle-height);border-radius:var(--mdc-switch-handle-shape, var(--mat-sys-corner-full))}[dir=rtl] .mdc-switch__handle{left:auto;right:0}.mat-mdc-slide-toggle .mdc-switch--unselected .mdc-switch__handle{width:var(--mat-switch-unselected-handle-size, 16px);height:var(--mat-switch-unselected-handle-size, 16px);margin:var(--mat-switch-unselected-handle-horizontal-margin, 0 8px)}.mat-mdc-slide-toggle .mdc-switch--unselected .mdc-switch__handle:has(.mdc-switch__icons){margin:var(--mat-switch-unselected-with-icon-handle-horizontal-margin, 0 4px)}.mat-mdc-slide-toggle .mdc-switch--selected .mdc-switch__handle{width:var(--mat-switch-selected-handle-size, 24px);height:var(--mat-switch-selected-handle-size, 24px);margin:var(--mat-switch-selected-handle-horizontal-margin, 0 24px)}.mat-mdc-slide-toggle .mdc-switch--selected .mdc-switch__handle:has(.mdc-switch__icons){margin:var(--mat-switch-selected-with-icon-handle-horizontal-margin, 0 24px)}.mat-mdc-slide-toggle .mdc-switch__handle:has(.mdc-switch__icons){width:var(--mat-switch-with-icon-handle-size, 24px);height:var(--mat-switch-with-icon-handle-size, 24px)}.mat-mdc-slide-toggle .mdc-switch:active:not(.mdc-switch--disabled) .mdc-switch__handle{width:var(--mat-switch-pressed-handle-size, 28px);height:var(--mat-switch-pressed-handle-size, 28px)}.mat-mdc-slide-toggle .mdc-switch--selected:active:not(.mdc-switch--disabled) .mdc-switch__handle{margin:var(--mat-switch-selected-pressed-handle-horizontal-margin, 0 22px)}.mat-mdc-slide-toggle .mdc-switch--unselected:active:not(.mdc-switch--disabled) .mdc-switch__handle{margin:var(--mat-switch-unselected-pressed-handle-horizontal-margin, 0 2px)}.mdc-switch--disabled.mdc-switch--selected .mdc-switch__handle::after{opacity:var(--mat-switch-disabled-selected-handle-opacity, 1)}.mdc-switch--disabled.mdc-switch--unselected .mdc-switch__handle::after{opacity:var(--mat-switch-disabled-unselected-handle-opacity, 0.38)}.mdc-switch__handle::before,.mdc-switch__handle::after{border:1px solid rgba(0,0,0,0);border-radius:inherit;box-sizing:border-box;content:"";width:100%;height:100%;left:0;position:absolute;top:0;transition:background-color 75ms 0ms cubic-bezier(0.4, 0, 0.2, 1),border-color 75ms 0ms cubic-bezier(0.4, 0, 0.2, 1);z-index:-1}@media(forced-colors: active){.mdc-switch__handle::before,.mdc-switch__handle::after{border-color:currentColor}}.mdc-switch--selected:enabled .mdc-switch__handle::after{background:var(--mdc-switch-selected-handle-color, var(--mat-sys-on-primary))}.mdc-switch--selected:enabled:hover:not(:focus):not(:active) .mdc-switch__handle::after{background:var(--mdc-switch-selected-hover-handle-color, var(--mat-sys-primary-container))}.mdc-switch--selected:enabled:focus:not(:active) .mdc-switch__handle::after{background:var(--mdc-switch-selected-focus-handle-color, var(--mat-sys-primary-container))}.mdc-switch--selected:enabled:active .mdc-switch__handle::after{background:var(--mdc-switch-selected-pressed-handle-color, var(--mat-sys-primary-container))}.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled.mdc-switch--selected:hover:not(:focus):not(:active) .mdc-switch__handle::after,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled.mdc-switch--selected:focus:not(:active) .mdc-switch__handle::after,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled.mdc-switch--selected:active .mdc-switch__handle::after,.mdc-switch--selected.mdc-switch--disabled .mdc-switch__handle::after{background:var(--mdc-switch-disabled-selected-handle-color, var(--mat-sys-surface))}.mdc-switch--unselected:enabled .mdc-switch__handle::after{background:var(--mdc-switch-unselected-handle-color, var(--mat-sys-outline))}.mdc-switch--unselected:enabled:hover:not(:focus):not(:active) .mdc-switch__handle::after{background:var(--mdc-switch-unselected-hover-handle-color, var(--mat-sys-on-surface-variant))}.mdc-switch--unselected:enabled:focus:not(:active) .mdc-switch__handle::after{background:var(--mdc-switch-unselected-focus-handle-color, var(--mat-sys-on-surface-variant))}.mdc-switch--unselected:enabled:active .mdc-switch__handle::after{background:var(--mdc-switch-unselected-pressed-handle-color, var(--mat-sys-on-surface-variant))}.mdc-switch--unselected.mdc-switch--disabled .mdc-switch__handle::after{background:var(--mdc-switch-disabled-unselected-handle-color, var(--mat-sys-on-surface))}.mdc-switch__handle::before{background:var(--mdc-switch-handle-surface-color)}.mdc-switch__shadow{border-radius:inherit;bottom:0;left:0;position:absolute;right:0;top:0}.mdc-switch:enabled .mdc-switch__shadow{box-shadow:var(--mdc-switch-handle-elevation-shadow)}.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:hover:not(:focus):not(:active) .mdc-switch__shadow,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:focus:not(:active) .mdc-switch__shadow,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:active .mdc-switch__shadow,.mdc-switch.mdc-switch--disabled .mdc-switch__shadow{box-shadow:var(--mdc-switch-disabled-handle-elevation-shadow)}.mdc-switch__ripple{left:50%;position:absolute;top:50%;transform:translate(-50%, -50%);z-index:-1;width:var(--mdc-switch-state-layer-size, 40px);height:var(--mdc-switch-state-layer-size, 40px)}.mdc-switch__ripple::after{content:"";opacity:0}.mdc-switch--disabled .mdc-switch__ripple::after{display:none}.mat-mdc-slide-toggle-disabled-interactive .mdc-switch__ripple::after{display:block}.mdc-switch:hover .mdc-switch__ripple::after{opacity:.04;transition:75ms opacity cubic-bezier(0, 0, 0.2, 1)}.mat-mdc-slide-toggle.mat-mdc-slide-toggle-focused .mdc-switch .mdc-switch__ripple::after{opacity:.12}.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:enabled:focus .mdc-switch__ripple::after,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:enabled:active .mdc-switch__ripple::after,.mat-mdc-slide-toggle-disabled-interactive.mdc-switch--disabled:enabled:hover:not(:focus) .mdc-switch__ripple::after,.mdc-switch--unselected:enabled:hover:not(:focus) .mdc-switch__ripple::after{background:var(--mdc-switch-unselected-hover-state-layer-color, var(--mat-sys-on-surface))}.mdc-switch--unselected:enabled:focus .mdc-switch__ripple::after{background:var(--mdc-switch-unselected-focus-state-layer-color, var(--mat-sys-on-surface))}.mdc-switch--unselected:enabled:active .mdc-switch__ripple::after{background:var(--mdc-switch-unselected-pressed-state-layer-color, var(--mat-sys-on-surface));opacity:var(--mdc-switch-unselected-pressed-state-layer-opacity, var(--mat-sys-pressed-state-layer-opacity));transition:opacity 75ms linear}.mdc-switch--selected:enabled:hover:not(:focus) .mdc-switch__ripple::after{background:var(--mdc-switch-selected-hover-state-layer-color, var(--mat-sys-primary))}.mdc-switch--selected:enabled:focus .mdc-switch__ripple::after{background:var(--mdc-switch-selected-focus-state-layer-color, var(--mat-sys-primary))}.mdc-switch--selected:enabled:active .mdc-switch__ripple::after{background:var(--mdc-switch-selected-pressed-state-layer-color, var(--mat-sys-primary));opacity:var(--mdc-switch-selected-pressed-state-layer-opacity, var(--mat-sys-pressed-state-layer-opacity));transition:opacity 75ms linear}.mdc-switch__icons{position:relative;height:100%;width:100%;z-index:1}.mdc-switch--disabled.mdc-switch--unselected .mdc-switch__icons{opacity:var(--mdc-switch-disabled-unselected-icon-opacity, 0.38)}.mdc-switch--disabled.mdc-switch--selected .mdc-switch__icons{opacity:var(--mdc-switch-disabled-selected-icon-opacity, 0.38)}.mdc-switch__icon{bottom:0;left:0;margin:auto;position:absolute;right:0;top:0;opacity:0;transition:opacity 30ms 0ms cubic-bezier(0.4, 0, 1, 1)}.mdc-switch--unselected .mdc-switch__icon{width:var(--mdc-switch-unselected-icon-size, 16px);height:var(--mdc-switch-unselected-icon-size, 16px);fill:var(--mdc-switch-unselected-icon-color, var(--mat-sys-surface-variant))}.mdc-switch--unselected.mdc-switch--disabled .mdc-switch__icon{fill:var(--mdc-switch-disabled-unselected-icon-color, var(--mat-sys-surface-variant))}.mdc-switch--selected .mdc-switch__icon{width:var(--mdc-switch-selected-icon-size, 16px);height:var(--mdc-switch-selected-icon-size, 16px);fill:var(--mdc-switch-selected-icon-color, var(--mat-sys-on-primary-container))}.mdc-switch--selected.mdc-switch--disabled .mdc-switch__icon{fill:var(--mdc-switch-disabled-selected-icon-color, var(--mat-sys-on-surface))}.mdc-switch--selected .mdc-switch__icon--on,.mdc-switch--unselected .mdc-switch__icon--off{opacity:1;transition:opacity 45ms 30ms cubic-bezier(0, 0, 0.2, 1)}.mat-mdc-slide-toggle{-webkit-user-select:none;user-select:none;display:inline-block;-webkit-tap-highlight-color:rgba(0,0,0,0);outline:0}.mat-mdc-slide-toggle .mat-mdc-slide-toggle-ripple,.mat-mdc-slide-toggle .mdc-switch__ripple::after{top:0;left:0;right:0;bottom:0;position:absolute;border-radius:50%;pointer-events:none}.mat-mdc-slide-toggle .mat-mdc-slide-toggle-ripple:not(:empty),.mat-mdc-slide-toggle .mdc-switch__ripple::after:not(:empty){transform:translateZ(0)}.mat-mdc-slide-toggle.mat-mdc-slide-toggle-focused .mat-focus-indicator::before{content:""}.mat-mdc-slide-toggle .mat-internal-form-field{color:var(--mat-switch-label-text-color, var(--mat-sys-on-surface));font-family:var(--mat-switch-label-text-font, var(--mat-sys-body-medium-font));line-height:var(--mat-switch-label-text-line-height, var(--mat-sys-body-medium-line-height));font-size:var(--mat-switch-label-text-size, var(--mat-sys-body-medium-size));letter-spacing:var(--mat-switch-label-text-tracking, var(--mat-sys-body-medium-tracking));font-weight:var(--mat-switch-label-text-weight, var(--mat-sys-body-medium-weight))}.mat-mdc-slide-toggle .mat-ripple-element{opacity:.12}.mat-mdc-slide-toggle .mat-focus-indicator::before{border-radius:50%}.mat-mdc-slide-toggle._mat-animation-noopable .mdc-switch__handle-track,.mat-mdc-slide-toggle._mat-animation-noopable .mdc-switch__icon,.mat-mdc-slide-toggle._mat-animation-noopable .mdc-switch__handle::before,.mat-mdc-slide-toggle._mat-animation-noopable .mdc-switch__handle::after,.mat-mdc-slide-toggle._mat-animation-noopable .mdc-switch__track::before,.mat-mdc-slide-toggle._mat-animation-noopable .mdc-switch__track::after{transition:none}.mat-mdc-slide-toggle .mdc-switch:enabled+.mdc-label{cursor:pointer}.mat-mdc-slide-toggle .mdc-switch--disabled+label{color:var(--mdc-switch-disabled-label-text-color)}'],encapsulation:2,changeDetection:0})}return t})();var PF=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({imports:[ac,mA,mA]})}return t})();var xI=class t{sessionState={};constructor(){}static \u0275fac=function(A){return new(A||t)};static \u0275cmp=O({type:t,selectors:[["app-state-tab"]],inputs:{sessionState:"sessionState"},standalone:!1,decls:3,vars:1,consts:[[1,"state-wrapper"],[3,"json"]],template:function(A,i){A&1&&(d(0,"div",0)(1,"div"),P(2,"ngx-json-viewer",1),h()()),A&2&&(D(2),L("json",i.sessionState))},dependencies:[ic],styles:[".state-wrapper[_ngcontent-%COMP%]{padding-left:25px;padding-right:25px;margin-top:16px}"]})};var YI=class t{constructor(e,A){this.el=e;this.renderer=A;this.sideDrawerMaxWidth=window.innerWidth/2}sideDrawerMinWidth=310;sideDrawerMaxWidth;resizeHandle=null;resizingEvent={isResizing:!1,startingCursorX:0,startingWidth:0};ngAfterViewInit(){this.resizeHandle=document.getElementsByClassName("resize-handler")[0],this.renderer.listen(this.resizeHandle,"mousedown",e=>this.onResizeHandleMouseDown(e)),document.documentElement.style.setProperty("--side-drawer-width","500px"),this.renderer.setStyle(this.el.nativeElement,"width","var(--side-drawer-width)")}onResizeHandleMouseDown(e){this.resizingEvent={isResizing:!0,startingCursorX:e.clientX,startingWidth:this.sideDrawerWidth},e.preventDefault()}onMouseMove(e){if(!this.resizingEvent.isResizing)return;let A=e.clientX-this.resizingEvent.startingCursorX,i=this.resizingEvent.startingWidth+A;this.sideDrawerWidth=i,this.renderer.addClass(document.body,"resizing")}onMouseUp(){this.resizingEvent.isResizing=!1,this.renderer.removeClass(document.body,"resizing")}onResize(){this.sideDrawerMaxWidth=window.innerWidth/2,this.sideDrawerWidth=this.sideDrawerWidth}set sideDrawerWidth(e){let A=Math.min(Math.max(e,this.sideDrawerMinWidth),this.sideDrawerMaxWidth);document.body.style.setProperty("--side-drawer-width",`${A}px`)}get sideDrawerWidth(){let e=getComputedStyle(document.body).getPropertyValue("--side-drawer-width"),A=parseInt(e,10);return isNaN(A)?500:A}static \u0275fac=function(A){return new(A||t)(V(q),V(ae))};static \u0275dir=T({type:t,selectors:[["","appResizableDrawer",""]],hostBindings:function(A,i){A&1&&G("mousemove",function(n){return i.onMouseMove(n)},!1,sh)("mouseup",function(){return i.onMouseUp()},!1,sh)("resize",function(){return i.onResize()},!1,Ey)},standalone:!1})};var fZ=["videoContainer"],pZ=["sideDrawer"],wZ=["autoScroll"],yZ=()=>[],MZ=(t,e)=>({"user-message":t,"bot-message":e}),RZ=t=>({"eval-fail":t}),kZ=(t,e)=>({"eval-pass":t,"eval-fail":e}),bZ=(t,e)=>({"font-style":t,color:e}),ZF=t=>({"background-color":t});function FZ(t,e){if(t&1){let A=rA();d(0,"span",25),G("click",function(){Y(A);let o=y();return J(o.toggleSidePanel())}),k(1,"left_panel_open"),h()}}function vZ(t,e){if(t&1&&(d(0,"mat-option",15),k(1),h()),t&2){let A=e.$implicit;L("value",A),D(),NA(A)}}function SZ(t,e){t&1&&fe(0,vZ,2,2,"mat-option",15,De),t&2&&pe(e)}function NZ(t,e){if(t&1&&(d(0,"mat-option",15),k(1),h()),t&2){let A=y();L("value",A.selectedAppControl.value),D(),NA(A.selectedAppControl.value)}}function GZ(t,e){t&1&&(d(0,"span",32),k(1,"Events"),h())}function LZ(t,e){t&1&&(d(0,"span",32),k(1,"State"),h())}function _Z(t,e){t&1&&(d(0,"span",32),k(1,"Artifacts"),h())}function KZ(t,e){t&1&&(d(0,"span",32),k(1,"Sessions"),h())}function UZ(t,e){t&1&&(d(0,"span",32),k(1,"Eval"),h())}function xZ(t,e){if(t&1){let A=rA();d(0,"mat-tab"),x(1,UZ,2,0,"ng-template",27),d(2,"app-eval-tab",33),G("shouldShowTab",function(o){Y(A);let n=y(2);return J(n.handleShouldShowEvalTab(o))})("sessionSelected",function(o){Y(A);let n=y(2);return J(n.updateWithSelectedSession(o))}),h()()}if(t&2){let A=y(2);D(2),L("appName",A.appName)("userId",A.userId)("sessionId",A.sessionId)}}function YZ(t,e){if(t&1){let A=rA();d(0,"div",16)(1,"mat-tab-group")(2,"mat-tab",26),x(3,GZ,2,0,"ng-template",27),d(4,"app-event-tab",28),G("selectedEvent",function(o){Y(A);let n=y();return J(n.selectEvent(o))}),h()(),d(5,"mat-tab"),x(6,LZ,2,0,"ng-template",27),P(7,"app-state-tab",29),h(),d(8,"mat-tab"),x(9,_Z,2,0,"ng-template",27),P(10,"app-artifact-tab",30),h(),d(11,"mat-tab"),x(12,KZ,2,0,"ng-template",27),d(13,"app-session-tab",31),G("sessionSelected",function(o){Y(A);let n=y();return J(n.updateWithSelectedSession(o))})("sessionReloaded",function(o){Y(A);let n=y();return J(n.updateSessionState(o))}),h()(),x(14,xZ,3,3,"mat-tab"),h()()}if(t&2){let A=y();D(4),L("eventsMap",A.eventData)("traceData",A.traceData),D(3),L("sessionState",A.currentSessionState),D(3),L("artifacts",A.artifacts),D(3),L("userId",A.userId)("appName",A.appName)("sessionId",A.sessionId),D(),_(A.shouldShowEvalTab()?14:-1)}}function JZ(t,e){if(t&1){let A=rA();d(0,"div",46),G("click",function(){Y(A);let o=y(2);return J(o.openViewImageDialog(o.rawSvgString))}),h()}if(t&2){let A=y(2);L("innerHtml",A.renderedEventGraph,Ca)}}function HZ(t,e){if(t&1){let A=rA();d(0,"div",17)(1,"div",34)(2,"div",35)(3,"mat-paginator",36),G("page",function(o){Y(A);let n=y();return J(n.handlePageEvent(o))}),h(),d(4,"button",37)(5,"mat-icon",38),G("click",function(){Y(A);let o=y();return J(o.closeSelectedEvent())}),k(6,"close"),h()()()(),d(7,"div")(8,"mat-tab-group")(9,"mat-tab",39)(10,"div",40),x(11,JZ,1,1,"div",41),h(),d(12,"div",42),P(13,"ngx-json-viewer",43),h()(),d(14,"mat-tab",44)(15,"div",42),P(16,"ngx-json-viewer",43),h()(),d(17,"mat-tab",45)(18,"div",42),P(19,"ngx-json-viewer",43),h()()()()()}if(t&2){let A=y();D(3),L("length",A.eventData.size)("pageSize",1)("pageIndex",A.selectedEventIndex),D(8),_(A.renderedEventGraph?11:-1),D(2),L("json",A.selectedEvent),D(3),L("json",A.llmRequest),D(3),L("json",A.llmResponse)}}function TZ(t,e){if(t&1){let A=rA();d(0,"div",20)(1,"div",47)(2,"div",48),k(3,"Session ID"),h(),d(4,"div",49),k(5),h()(),d(6,"div",50)(7,"div",51)(8,"mat-slide-toggle",52),G("change",function(){Y(A);let o=y();return J(o.toggleSse())}),k(9," Token Streaming "),h()(),P(10,"mat-divider",53),d(11,"div",54)(12,"div",55),G("click",function(){Y(A);let o=y();return J(o.onNewSessionClick())}),d(13,"mat-icon"),k(14,"add"),h(),k(15," New Session "),h(),d(16,"span",56),G("click",function(){Y(A);let o=y();return J(o.deleteSession(o.sessionId))}),k(17," delete "),h(),d(18,"span",57),G("click",function(){Y(A);let o=y();return J(o.exportSession())}),k(19," download "),h()()()()}if(t&2){let A=y();D(5),NA(A.sessionId),D(3),L("checked",A.enableSseIndicator()),D(2),L("vertical",!0)}}function OZ(t,e){t&1&&(d(0,"div",58)(1,"span"),k(2,"Loading agents, please wait..."),h()())}function PZ(t,e){t&1&&(d(0,"span"),k(1,"Welcome to ADK!"),P(2,"br"),k(3," Select an agent on the left to begin with."),h())}function ZZ(t,e){if(t&1&&(k(0," Error message: "),P(1,"br"),d(2,"pre",60),k(3),h()),t&2){let A=y(4);D(3),NA(A.loadingError())}}function qZ(t,e){t&1&&(d(0,"pre",59),k(1,"Warning: No agents found in current folder."),h())}function VZ(t,e){if(t&1&&(d(0,"div"),k(1," Failed to load agents. To get started, run "),d(2,"pre"),k(3,"adk web"),h(),k(4," in the folder that contains the agents."),P(5,"br"),x(6,ZZ,4,1)(7,qZ,2,0,"pre",59),h()),t&2){let A=y(3);D(6),_(A.loadingError()?6:7)}}function WZ(t,e){if(t&1&&(d(0,"div",58),x(1,PZ,4,0,"span"),To(2,"async"),x(3,VZ,8,1,"div"),h()),t&2){let A=y(2);D(),_((br(2,1,A.apps$)||OB(3,yZ)).length>0?1:3)}}function zZ(t,e){if(t&1&&x(0,OZ,3,0,"div",58)(1,WZ,4,4,"div",58),t&2){let A=y();_(A.isLoadingApps()?0:1)}}function jZ(t,e){if(t&1){let A=rA();d(0,"button",61),G("click",function(){Y(A);let o=y();return J(o.openDialog())}),d(1,"mat-icon"),k(2,"priority_high"),h()()}}function XZ(t,e){if(t&1){let A=rA();d(0,"button",72),G("click",function(){Y(A);let o=y().$index,n=y(2);return J(n.clickEvent(o))}),d(1,"mat-icon",73),k(2,"robot_2"),h()()}if(t&2){let A=y(3);L("matTooltip",A.selectedAppControl.value)}}function $Z(t,e){t&1&&P(0,"mat-progress-bar",65)}function Aq(t,e){if(t&1&&P(0,"img",75),t&2){let A=y().$implicit;L("src",A.url,Zt)}}function eq(t,e){if(t&1&&(d(0,"mat-icon"),k(1,"insert_drive_file"),h(),d(2,"a",76),k(3),h()),t&2){let A=y().$implicit;D(2),L("href",A.url,Zt),D(),NA(A.file.name)}}function tq(t,e){if(t&1&&(d(0,"div",74),x(1,Aq,1,1,"img",75)(2,eq,4,2),h()),t&2){let A=e.$implicit;D(),_(A.file.type.startsWith("image/")?1:-1),D(),_(A.file.type.startsWith("image/")?-1:2)}}function iq(t,e){if(t&1&&(d(0,"div",66),fe(1,tq,3,2,"div",74,De),h()),t&2){let A=y().$implicit;D(),pe(A.attachments)}}function oq(t,e){t&1&&(d(0,"div",67),k(1,"Thought"),h())}function nq(t,e){if(t&1&&P(0,"markdown",68),t&2){let A=y().$implicit;L("data",A.text)("ngStyle",wn(2,bZ,A.thought?"italic":"normal",A.thought?"#9aa0a6":"white"))}}function gq(t,e){if(t&1&&(d(0,"div"),P(1,"div",77),h()),t&2){let A=y().$implicit,i=y(2);D(),L("innerHTML",i.renderGooglerSearch(A.renderedContent),Ca)}}function rq(t,e){if(t&1&&(d(0,"code"),k(1),h()),t&2){let A=y().$implicit;D(),YA(" ",A.executableCode.code," ")}}function sq(t,e){if(t&1&&(d(0,"div")(1,"div"),k(2),h(),d(3,"div"),k(4),h()()),t&2){let A=y().$implicit;D(2),YA("Outcome: ",A.codeExecutionResult.outcome,""),D(2),YA("Output: ",A.codeExecutionResult.output,"")}}function aq(t,e){if(t&1){let A=rA();d(0,"div",78)(1,"img",79),G("click",function(){Y(A);let o=y(3).$implicit,n=y(2);return J(n.openViewImageDialog(o.inlineData.data))}),h()()}if(t&2){let A=y(3).$implicit;D(),L("src",A.inlineData.data,Zt)}}function Iq(t,e){if(t&1&&(d(0,"div"),P(1,"app-audio-player",80),h()),t&2){let A=y(3).$implicit;D(),L("base64data",A.inlineData.data)}}function Cq(t,e){if(t&1){let A=rA();d(0,"div")(1,"div",81)(2,"mat-icon"),k(3,"description"),h(),d(4,"button",82),G("click",function(){Y(A);let o=y(3).$implicit,n=y(2);return J(n.openBase64InNewTab(o.inlineData.data,o.inlineData.mimeType))}),k(5),h()()()}if(t&2){let A=y(3).$implicit;D(5),YA(" ",A.inlineData.name," ")}}function Bq(t,e){if(t&1){let A=rA();d(0,"div")(1,"button",82),G("click",function(){Y(A);let o=y(3).$implicit,n=y(2);return J(n.openBase64InNewTab(o.inlineData.data,o.inlineData.mimeType))}),k(2),h()()}if(t&2){let A=y(3).$implicit;D(2),YA(" ",A.inlineData.name," ")}}function Qq(t,e){if(t&1&&(d(0,"div")(1,"div"),x(2,aq,2,1,"div",78)(3,Iq,2,1,"div")(4,Cq,6,1,"div")(5,Bq,3,1,"div"),h()()),t&2){let A,i=y(2).$implicit,o=y(2);D(2),_((A=i.inlineData.mediaType)===o.MediaType.IMAGE?2:A===o.MediaType.AUDIO?3:A===o.MediaType.TEXT?4:5)}}function Eq(t,e){if(t&1){let A=rA();d(0,"div")(1,"img",83),G("click",function(){Y(A);let o=y(3).$implicit,n=y(2);return J(n.openViewImageDialog(o.inlineData.data))}),h()()}if(t&2){let A=y(3).$implicit;D(),L("src",A.inlineData.data,Zt)}}function cq(t,e){if(t&1&&(d(0,"div")(1,"mat-icon"),k(2,"insert_drive_file"),h(),d(3,"a",76),k(4),h()()),t&2){let A=y(3).$implicit;D(3),L("href",A.inlineData.data,Zt),D(),NA(A.inlineData.displayName)}}function lq(t,e){if(t&1&&(d(0,"div"),x(1,Eq,2,1,"div")(2,cq,5,2,"div"),h()),t&2){let A=y(2).$implicit;D(),_(A.inlineData.mimeType.startsWith("image/")?1:2)}}function dq(t,e){if(t&1&&x(0,Qq,6,1,"div")(1,lq,3,1,"div"),t&2){let A=y().$implicit;_(A.role==="bot"?0:1)}}function hq(t,e){if(t&1){let A=rA();d(0,"button",84),G("click",function(){Y(A);let o=y().$index,n=y(2);return J(n.clickEvent(o))}),d(1,"mat-icon"),k(2,"bolt"),h(),k(3),h()}if(t&2){let A=y().$implicit;D(3),YA(" ",A.functionCall.name," ")}}function uq(t,e){if(t&1){let A=rA();d(0,"button",84),G("click",function(){Y(A);let o=y().$index,n=y(2);return J(n.clickEvent(o))}),d(1,"mat-icon"),k(2,"check"),h(),k(3),h()}if(t&2){let A=y().$implicit;D(3),YA(" ",A.functionResponse.name," ")}}function mq(t,e){if(t&1&&(d(0,"div",70)(1,"div",85)(2,"div",86),k(3,"Actual tool uses:"),h(),P(4,"ngx-json-viewer",43),h(),d(5,"div",87)(6,"div",86),k(7,"Expected tool uses:"),h(),P(8,"ngx-json-viewer",43),h()()),t&2){let A=y().$implicit;D(4),L("json",A.actualInvocationToolUses),D(4),L("json",A.expectedInvocationToolUses)}}function Dq(t,e){t&1&&(d(0,"button",37)(1,"mat-icon"),k(2,"person"),h()())}function fq(t,e){if(t&1&&(d(0,"div",62),x(1,XZ,3,1,"button",63),d(2,"mat-card",64),x(3,$Z,1,0,"mat-progress-bar",65)(4,iq,3,0,"div",66),d(5,"div"),x(6,oq,2,0,"div",67),d(7,"div"),x(8,nq,1,5,"markdown",68),h(),x(9,gq,2,1,"div"),h(),x(10,rq,2,1,"code")(11,sq,5,2,"div")(12,dq,2,1)(13,hq,4,1,"button",69)(14,uq,4,1,"button",69)(15,mq,9,2,"div",70),h(),d(16,"div",62)(17,"span",71),k(18),h(),d(19,"span"),k(20),h()(),x(21,Dq,3,0,"button",37),h()),t&2){let A=e.$implicit;L("ngClass",wn(18,MZ,A.role==="user",A.role==="bot")),D(),_(A.role==="bot"?1:-1),D(),L("ngClass",pn(21,RZ,A.evalStatus===2)),D(),_(A.isLoading?3:-1),D(),_(A.attachments?4:-1),D(2),_(A.thought?6:-1),D(2),_(A.text?8:-1),D(),_(A.renderedContent?9:-1),D(),_(A.executableCode?10:-1),D(),_(A.codeExecutionResult?11:-1),D(),_(A.inlineData?12:-1),D(),_(A.functionCall?13:-1),D(),_(A.functionResponse?14:-1),D(),_(A.actualInvocationToolUses&&A.evalStatus===2?15:-1),D(),L("ngClass",wn(23,kZ,A.evalStatus===1,A.evalStatus===2)),D(2),NA(A.evalStatus===1?"check":A.evalStatus===2?"close":""),D(2),NA(A.evalStatus===1?"Pass":A.evalStatus===2?"Fail":""),D(),_(A.role==="user"?21:-1)}}function pq(t,e){if(t&1&&(d(0,"div",23,1),P(2,"div",null,2),fe(4,fq,22,26,"div",62,De),h()),t&2){let A=y();D(4),pe(A.messages)}}function wq(t,e){if(t&1){let A=rA();d(0,"div",95),P(1,"img",97),d(2,"button",98),G("click",function(){Y(A);let o=y().$index,n=y(3);return J(n.removeFile(o))}),d(3,"mat-icon",99),k(4,"close"),h()()()}if(t&2){let A=y().$implicit;D(),L("src",A.url,Zt)}}function yq(t,e){if(t&1){let A=rA();d(0,"div",96)(1,"button",98),G("click",function(){Y(A);let o=y().$index,n=y(3);return J(n.removeFile(o))}),d(2,"mat-icon",99),k(3,"close"),h()(),d(4,"div",100)(5,"mat-icon"),k(6,"insert_drive_file"),h(),d(7,"span"),k(8),h()()()}if(t&2){let A=y().$implicit;D(8),NA(A.file.name)}}function Mq(t,e){if(t&1&&(d(0,"div"),x(1,wq,5,1,"div",95)(2,yq,9,1,"div",96),h()),t&2){let A=e.$implicit;D(),_(A.file.type.startsWith("image/")?1:-1),D(),_(A.file.type.startsWith("image/")?-1:2)}}function Rq(t,e){if(t&1&&(d(0,"div",90),fe(1,Mq,3,2,"div",null,De),h()),t&2){let A=y(2);D(),pe(A.selectedFiles)}}function kq(t,e){if(t&1){let A=rA();d(0,"div",24)(1,"input",88,3),G("change",function(o){Y(A);let n=y();return J(n.onFileSelect(o))}),h(),d(3,"mat-form-field",89),x(4,Rq,3,0,"div",90),d(5,"textarea",91),Vt("ngModelChange",function(o){Y(A);let n=y();return si(n.userInput,o)||(n.userInput=o),J(o)}),G("keydown.enter",function(o){Y(A);let n=y();return J(n.sendMessage(o))}),h(),d(6,"div",92)(7,"button",93),G("click",function(){Y(A);let o=_e(2);return J(o.click())}),d(8,"mat-icon"),k(9,"attach_file"),h()(),d(10,"div")(11,"button",94),G("click",function(){Y(A);let o=y();return J(o.toggleAudioRecording())}),d(12,"mat-icon"),k(13,"mic"),h()(),d(14,"button",94),G("click",function(){Y(A);let o=y();return J(o.toggleVideoRecording())}),d(15,"mat-icon"),k(16,"videocam"),h()()()()()()}if(t&2){let A=y();D(4),_(A.selectedFiles.length&&A.appName!=""?4:-1),D(),qt("ngModel",A.userInput),D(6),L("ngStyle",pn(6,ZF,A.isAudioRecording?"rgb(234, 67, 53)":"rgb(51, 53, 55)"))("matTooltip",A.isAudioRecording?"Turn off microphone":"Use microphone"),D(3),L("ngStyle",pn(8,ZF,A.isVideoRecording?"rgb(234, 67, 53)":"rgb(51, 53, 55)"))("matTooltip",A.isVideoRecording?"Turn off camera":"Use camera")}}function bq(t){for(t=t.replace(/-/g,"+").replace(/_/g,"/");t.length%4!==0;)t+="=";return t}var FD=class extends Ng{nextPageLabel="Next Event";previousPageLabel="Previous Event";firstPageLabel="First Event";lastPageLabel="Last Event";getRangeLabel=(e,A,i)=>i===0?`Event 0 of ${i}`:(i=Math.max(i,0),`Event ${e*A+1} of ${i}`)},qF="Restarting bidirectional streaming is not currently supported. Please refresh the page or start a new session.",JI=class t{constructor(e,A,i,o,n,g,r,s,a,Q){this.sanitizer=e;this.sessionService=A;this.artifactService=i;this.audioService=o;this.webSocketService=n;this.videoService=g;this.dialog=r;this.eventService=s;this.route=a;this.downloadService=Q}videoContainer;sideDrawer;eventTabComponent;sessionTab;evalTab;scrollContainer;_snackBar=B(Xk);shouldShowEvalTab=gt(!0);enableSseIndicator=gt(!1);videoElement;currentMessage="";messages=[];lastTextChunk="";streamingTextMessage=null;artifacts=[];userInput="";userId="user";appName="";sessionId="";isAudioRecording=!1;isVideoRecording=!1;longRunningEvents=[];functionCallEventId="";redirectUri=ct.getBaseUrlWithoutPath();showSidePanel=!0;useSse=!1;currentSessionState={};messagesSubject=new $A([]);streamingTextMessageSubject=new $A(null);scrollInterruptedSubject=new $A(!0);sessionHasUsedBidi=new Set;eventData=new Map;traceData=[];eventMessageIndexArray=[];renderedEventGraph;rawSvgString=null;selectedEvent=void 0;selectedEventIndex=void 0;llmRequest=void 0;llmResponse=void 0;llmRequestKey="gcp.vertex.agent.llm_request";llmResponseKey="gcp.vertex.agent.llm_response";getMediaTypeFromMimetype=OE;selectedFiles=[];previousMessageCount=0;openBase64InNewTab=Tm;MediaType=wI;router=B(Bo);activatedRoute=B(Ii);selectedAppControl=new RQ("",{nonNullable:!0});agentService=B(Un);isLoadingApps=gt(!1);loadingError=gt("");apps$=iA([]).pipe(Ce(()=>{this.isLoadingApps.set(!0),this.selectedAppControl.disable()}),Ie(()=>this.agentService.listApps().pipe(Oe(e=>(this.loadingError.set(e.message),iA(void 0))))),ue(1),Ce(e=>{this.isLoadingApps.set(!1),this.selectedAppControl.enable(),e?.length==1&&this.router.navigate([],{relativeTo:this.route,queryParams:{app:e[0]}})}),Go());ngOnInit(){if(this.syncSelectedAppFromUrl(),this.updateSelectedAppUrl(),this.webSocketService.onCloseReason().subscribe(i=>{let o=`Please check server log for full details: 
`+i;this.openSnackBar(o,"OK")}),new URL(window.location.href).searchParams.has("code")){let i=window.location.href;window.opener?.postMessage({authResponseUrl:i},window.origin),window.close()}this.agentService.getApp().subscribe(i=>{this.appName=i}),this.agentService.getLoadingState().subscribe(i=>{i?(this.messages.push({role:"bot",isLoading:!0}),this.messagesSubject.next(this.messages)):this.messages[this.messages.length-1]&&this.messages[this.messages.length-1].isLoading&&(this.messages.pop(),this.messagesSubject.next(this.messages))}),Rt([this.messagesSubject,this.scrollInterruptedSubject,this.streamingTextMessageSubject]).subscribe(([i,o,n])=>{o||setTimeout(()=>{this.scrollToBottom()},100)})}ngAfterViewInit(){this.showSidePanel=!0,this.sideDrawer.open()}scrollToBottom(){setTimeout(()=>{this.scrollContainer.nativeElement.scrollTo({top:this.scrollContainer.nativeElement.scrollHeight,behavior:"smooth"})})}selectApp(e){e!=this.appName&&(this.agentService.setApp(e),this.createSession(),this.eventData=new Map,this.eventMessageIndexArray=[],this.messages=[],this.artifacts=[],this.userInput="",this.longRunningEvents=[])}createSession(){this.sessionService.createSession(this.userId,this.appName).subscribe(e=>{this.currentSessionState=e.state,this.sessionId=e.id,this.sessionTab.refreshSession()})}sendMessage(e){return $e(this,null,function*(){if(this.messages.length===0&&(this.scrollContainer.nativeElement.addEventListener("wheel",()=>{this.scrollInterruptedSubject.next(!0)}),this.scrollContainer.nativeElement.addEventListener("touchmove",()=>{this.scrollInterruptedSubject.next(!0)})),this.scrollInterruptedSubject.next(!1),e.preventDefault(),!this.userInput.trim())return;if(this.messages.push({role:"user",text:this.userInput}),this.messagesSubject.next(this.messages),this.selectedFiles.length>0){let o=this.selectedFiles.map(n=>({file:n.file,url:n.url}));this.messages.push({role:"user",attachments:o}),this.messagesSubject.next(this.messages)}let A={appName:this.appName,userId:this.userId,sessionId:this.sessionId,newMessage:{role:"user",parts:yield this.getUserMessageParts()},streaming:this.useSse};this.selectedFiles=[];let i=this.eventMessageIndexArray.length-1;this.streamingTextMessage=null,this.agentService.runSse(A).subscribe({next:o=>$e(this,null,function*(){if(this.agentService.getLoadingState().next(!1),o.startsWith('{"error"')){this.openSnackBar(o,"OK");return}let n=JSON.parse(o);if(n.error){this.openSnackBar(n.error,"OK");return}if(n.content)for(let g of n.content.parts)i+=1,this.processPart(n,g,i)}),error:o=>console.error("SSE error:",o),complete:()=>{this.streamingTextMessage=null,this.sessionTab.reloadSession(this.sessionId),this.eventService.getTrace(this.sessionId).pipe(Oe(o=>o.status===404?iA(null):iA([]))).subscribe(o=>{this.traceData=o})}}),this.userInput=""})}processPart(e,A,i){let o=e.groundingMetadata?.searchEntryPoint?.renderedContent;if(A.text){let n=A.text;if(this.streamingTextMessage){if(o&&(this.streamingTextMessage.renderedContent=e.groundingMetadata.searchEntryPoint.renderedContent),n==this.streamingTextMessage.text){this.storeEvents(A,e,i),this.eventMessageIndexArray[i]=n,this.streamingTextMessage=null;return}this.streamingTextMessage.text+=n,this.streamingTextMessageSubject.next(this.streamingTextMessage)}else if(this.streamingTextMessage={role:"bot",text:this.processThoughtText(n),thought:!!A.thought,eventId:e.id},o&&(this.streamingTextMessage.renderedContent=e.groundingMetadata.searchEntryPoint.renderedContent),this.messages.push(this.streamingTextMessage),this.messagesSubject.next(this.messages),!this.useSse){this.storeEvents(A,e,i),this.eventMessageIndexArray[i]=n,this.streamingTextMessage=null;return}}else this.storeEvents(A,e,i),this.storeMessage(A,e,i)}getUserMessageParts(){return $e(this,null,function*(){let e=[{text:`${this.userInput}`}];if(this.selectedFiles.length>0)for(let A of this.selectedFiles)e.push({inlineData:{displayName:A.file.name,data:yield this.readFileAsBytes(A.file),mimeType:A.file.type}});return e})}readFileAsBytes(e){return new Promise((A,i)=>{let o=new FileReader;o.onload=n=>{let g=n.target.result.split(",")[1];A(g)},o.onerror=i,o.readAsDataURL(e)})}updateRedirectUri(e,A){try{let i=new URL(e);return i.searchParams.set("redirect_uri",A),i.toString()}catch(i){return console.warn("Failed to update redirect URI: ",i),e}}storeMessage(e,A,i){if(A.longRunningToolIds&&A.longRunningToolIds.length>0){this.getAsyncFunctionsFromParts(A.longRunningToolIds,A.content.parts);let o=this.longRunningEvents[0];if(o.args.authConfig&&o.args.authConfig.exchangedAuthCredential&&o.args.authConfig.exchangedAuthCredential.oauth2){let n=o.args.authConfig.exchangedAuthCredential.oauth2.authUri,g=this.updateRedirectUri(n,this.redirectUri);this.openOAuthPopup(g).then(r=>{this.functionCallEventId=A.id,this.sendOAuthResponse(o,r,this.redirectUri)}).catch(r=>{console.error("OAuth Error:",r)})}else this.functionCallEventId=A.id}if(A.actions&&A.actions.artifactDelta)for(let o in A.actions.artifactDelta)A.actions.artifactDelta.hasOwnProperty(o)&&this.renderArtifact(o,A.actions.artifactDelta[o]);if(e.inlineData){let o=this.formatBase64Data(e.inlineData.data,e.inlineData.mimeType);this.messages.push({role:A.author==="user"?"user":"bot",inlineData:{displayName:e.inlineData.displayName,data:o,mimeType:e.inlineData.mimeType}}),this.messagesSubject.next(this.messages),this.eventMessageIndexArray[i]=e.inlineData}else if(e.text){let o={role:A.author==="user"?"user":"bot",text:e.text,evalStatus:A.evalStatus,actualInvocationToolUses:A.actualInvocationToolUses,expectedInvocationToolUses:A.expectedInvocationToolUses};A.groundingMetadata&&A.groundingMetadata.searchEntryPoint&&A.groundingMetadata.searchEntryPoint.renderedContent&&(o.renderedContent=A.groundingMetadata.searchEntryPoint.renderedContent),this.messages.push(o),this.messagesSubject.next(this.messages),this.eventMessageIndexArray[i]=e.text}else if(e.functionCall)this.messages.push({role:A.author==="user"?"user":"bot",functionCall:e.functionCall,eventId:A.id,evalStatus:A.evalStatus,actualInvocationToolUses:A.actualInvocationToolUses,expectedInvocationToolUses:A.expectedInvocationToolUses}),this.messagesSubject.next(this.messages),this.eventMessageIndexArray[i]=e.functionCall;else if(e.functionResponse)this.messages.push({role:A.author==="user"?"user":"bot",functionResponse:e.functionResponse,eventId:A.id,evalStatus:A.evalStatus,actualInvocationToolUses:A.actualInvocationToolUses,expectedInvocationToolUses:A.expectedInvocationToolUses}),this.messagesSubject.next(this.messages),this.eventMessageIndexArray[i]=e.functionResponse;else if(e.executableCode)this.messages.push({role:A.author==="user"?"user":"bot",executableCode:e.executableCode,evalStatus:A.evalStatus,actualInvocationToolUses:A.actualInvocationToolUses,expectedInvocationToolUses:A.expectedInvocationToolUses}),this.messagesSubject.next(this.messages),this.eventMessageIndexArray[i]=e.executableCode;else if(e.codeExecutionResult&&(this.messages.push({role:A.author==="user"?"user":"bot",codeExecutionResult:e.codeExecutionResult,evalStatus:A.evalStatus,actualInvocationToolUses:A.actualInvocationToolUses,expectedInvocationToolUses:A.expectedInvocationToolUses}),this.eventMessageIndexArray[i]=e.codeExecutionResult,A.actions&&A.actions.artifact_delta))for(let o in A.actions.artifact_delta)A.actions.artifact_delta.hasOwnProperty(o)&&this.renderArtifact(o,A.actions.artifact_delta[o])}formatBase64Data(e,A){let i=bq(e);return`data:${A};base64,${i}`}renderArtifact(e,A){this.messages.push({role:"bot",inlineData:{data:"",mimeType:"image/png"}}),this.messagesSubject.next(this.messages);let i=this.messages.length-1;this.artifactService.getArtifactVersion(this.userId,this.appName,this.sessionId,e,A).subscribe(o=>{let n=o.inlineData.mimeType,g=this.formatBase64Data(o.inlineData.data,n),r=OE(n),s={name:this.createDefaultArtifactName(n),data:g,mimeType:n,mediaType:r};this.messages[i]={role:"bot",inlineData:s},this.artifacts=[...this.artifacts,{id:e,data:g,mimeType:n,versionId:A,mediaType:OE(n)}]})}storeEvents(e,A,i){let o="";e.text?o+="text:"+e.text:e.functionCall?o+="functionCall:"+e.functionCall.name:e.functionResponse?o+="functionResponse:"+e.functionResponse.name:e.executableCode?o+="executableCode:"+e.executableCode.code.slice(0,10):e.codeExecutionResult&&(o+="codeExecutionResult:"+e.codeExecutionResult.outcome),A.title=o,this.eventData.set(A.id,A),this.eventData=new Map(this.eventData)}sendOAuthResponse(e,A,i){this.longRunningEvents.pop();let o={appName:this.appName,userId:this.userId,sessionId:this.sessionId,newMessage:{role:"user",parts:[]}};var n=structuredClone(e.args.authConfig);n.exchangedAuthCredential.oauth2.authResponseUri=A,n.exchangedAuthCredential.oauth2.redirectUri=i,o.functionCallEventId=this.functionCallEventId,o.newMessage.parts.push({function_response:{id:e.id,name:e.name,response:n}}),this.agentService.run(o).subscribe(g=>{this.processRunResponse(g)})}processRunResponse(e){let A=this.eventMessageIndexArray.length-1;for(let i of e)if(i.content)for(let o of i.content.parts)A+=1,this.processPart(i,o,A)}openDialog(){this.dialog.open(vI,{width:"600px",data:{event:this.longRunningEvents[0],appName:this.appName,userId:this.userId,sessionId:this.sessionId,functionCallEventId:this.functionCallEventId}}).afterClosed().subscribe(A=>{A&&(this.removeFinishedLongRunningEvents(A.events),this.processRunResponse(A.response))})}removeFinishedLongRunningEvents(e){let A=new Set(e.map(i=>i.id));this.longRunningEvents=this.longRunningEvents.filter(i=>!A.has(i.id))}clickEvent(e){let A=this.messages[e].eventId;this.sideDrawer.open(),this.showSidePanel=!0,this.selectedEvent=this.eventData.get(A),this.selectedEventIndex=this.getIndexOfKeyInMap(A),this.eventService.getEventTrace(this.selectedEvent.id).subscribe(i=>{this.llmRequest=JSON.parse(i[this.llmRequestKey]),this.llmResponse=JSON.parse(i[this.llmResponseKey])}),this.eventService.getEvent(this.userId,this.appName,this.sessionId,this.selectedEvent.id).subscribe(i=>$e(this,null,function*(){if(!i.dotSrc){this.renderedEventGraph=void 0;return}let o=i.dotSrc,g=(yield Um()).renderString(o,{format:"svg",engine:"dot"});this.rawSvgString=g,this.renderedEventGraph=this.sanitizer.bypassSecurityTrustHtml(g)}))}userMessagesLength(e){return this.messages.slice(0,e).filter(A=>A.role=="user").length}ngOnDestroy(){this.webSocketService.closeConnection()}onAppSelection(e){this.isAudioRecording&&(this.stopAudioRecording(),this.isAudioRecording=!1),this.isVideoRecording&&(this.stopVideoRecording(),this.isVideoRecording=!1)}toggleAudioRecording(){this.isAudioRecording?this.stopAudioRecording():this.startAudioRecording()}startAudioRecording(){if(this.sessionHasUsedBidi.has(this.sessionId)){this.openSnackBar(qF,"OK");return}this.isAudioRecording=!0;let e=window.location.protocol==="https:"?"wss":"ws";this.webSocketService.connect(`${e}://${ct.getWSServerUrl()}/run_live?app_name=${this.appName}&user_id=${this.userId}&session_id=${this.sessionId}`),this.audioService.startRecording(),this.messages.push({role:"user",text:"Speaking..."}),this.messages.push({role:"bot",text:"Speaking..."}),this.messagesSubject.next(this.messages),this.sessionHasUsedBidi.add(this.sessionId)}stopAudioRecording(){this.audioService.stopRecording(),this.webSocketService.closeConnection(),this.isAudioRecording=!1}toggleVideoRecording(){this.isVideoRecording?this.stopVideoRecording():this.startVideoRecording()}startVideoRecording(){if(this.sessionHasUsedBidi.has(this.sessionId)){this.openSnackBar(qF,"OK");return}this.isVideoRecording=!0;let e=window.location.protocol==="https:"?"wss":"ws";this.webSocketService.connect(`${e}://${ct.getWSServerUrl()}/run_live?app_name=${this.appName}&user_id=${this.userId}&session_id=${this.sessionId}`),this.videoService.startRecording(this.videoContainer),this.audioService.startRecording(),this.messages.push({role:"user",text:"Speaking..."}),this.messagesSubject.next(this.messages),this.sessionHasUsedBidi.add(this.sessionId)}stopVideoRecording(){this.audioService.stopRecording(),this.videoService.stopRecording(this.videoContainer),this.webSocketService.closeConnection(),this.isVideoRecording=!1}getAsyncFunctionsFromParts(e,A){for(let i of A)i.functionCall&&e.includes(i.functionCall.id)&&this.longRunningEvents.push(i.functionCall)}openOAuthPopup(e){return new Promise((A,i)=>{if(!window.open(e,"oauthPopup","width=600,height=700")){i("Popup blocked!");return}window.addEventListener("message",n=>{if(n.origin!==window.location.origin)return;let{authResponseUrl:g}=n.data;g?A(g):i("OAuth failed")},{once:!0})})}toggleSidePanel(){this.showSidePanel?this.sideDrawer.close():this.sideDrawer.open(),this.showSidePanel=!this.showSidePanel}handleShouldShowEvalTab(e){this.shouldShowEvalTab.set(e)}handleEvalNotInstalled(e){e&&this.openSnackBar(e,"OK")}updateWithSelectedSession(e){if(!e||!e.id||!e.events||!e.state)return;this.sessionId=e.id,this.currentSessionState=e.state,this.eventData.clear(),this.eventMessageIndexArray=[],this.messages=[],this.artifacts=[];let A=0;e.events.forEach(i=>{i.content?.parts?.forEach(o=>{this.storeMessage(o,i,A),A+=1,i.author&&i.author!=="user"&&this.storeEvents(o,i,A)})}),this.eventService.getTrace(this.sessionId).subscribe(i=>{this.traceData=i})}updateSessionState(e){this.currentSessionState=e.state}onNewSessionClick(){this.createSession(),this.eventData.clear(),this.eventMessageIndexArray=[],this.messages=[],this.artifacts=[],this.evalTab.showEvalHistory&&this.evalTab.toggleEvalHistoryButton()}onFileSelect(e){let A=e.target;if(A.files)for(let i=0;i<A.files.length;i++){let o=A.files[i],n=URL.createObjectURL(o);this.selectedFiles.push({file:o,url:n})}A.value=""}removeFile(e){URL.revokeObjectURL(this.selectedFiles[e].url),this.selectedFiles.splice(e,1)}toggleSse(){this.useSse=!this.useSse}selectEvent(e){this.selectedEvent=this.eventData.get(e),this.selectedEventIndex=this.getIndexOfKeyInMap(e),this.eventService.getEventTrace(this.selectedEvent.id).subscribe(A=>{this.llmRequest=JSON.parse(A[this.llmRequestKey]),this.llmResponse=JSON.parse(A[this.llmResponseKey])}),this.eventService.getEvent(this.userId,this.appName,this.sessionId,this.selectedEvent.id).subscribe(A=>$e(this,null,function*(){if(!A.dotSrc){this.renderedEventGraph=void 0;return}let i=A.dotSrc,n=(yield Um()).renderString(i,{format:"svg",engine:"dot"});this.rawSvgString=n,this.renderedEventGraph=this.sanitizer.bypassSecurityTrustHtml(n)}))}deleteSession(e){let A={title:"Confirm delete",message:`Are you sure you want to delete this session ${this.sessionId}?`,confirmButtonText:"Delete",cancelButtonText:"Cancel"};this.dialog.open(SI,{width:"600px",data:A}).afterClosed().subscribe(o=>{o&&this.sessionService.deleteSession(this.userId,this.appName,e).subscribe(n=>{let g=this.sessionTab.refreshSession(e);g?this.sessionTab.getSession(g.id):window.location.reload()})})}syncSelectedAppFromUrl(){Rt([this.router.events.pipe(kA(e=>e instanceof Ai),sA(()=>this.activatedRoute.snapshot.queryParams)),this.apps$]).subscribe(([e,A])=>{if(A&&A.length){let i=e.app;i&&A.includes(i)?this.selectedAppControl.setValue(i):i&&this.openSnackBar(`Agent '${i}' not found`,"OK")}})}updateSelectedAppUrl(){this.selectedAppControl.valueChanges.pipe(wi(),kA(Boolean)).subscribe(e=>{this.selectApp(e);let A=this.activatedRoute.snapshot.queryParams.app;e!==A&&this.router.navigate([],{queryParams:{app:e},queryParamsHandling:"merge"})})}handlePageEvent(e){if(e.pageIndex>=0){let A=this.getKeyAtIndexInMap(e.pageIndex);A&&this.selectEvent(A)}}closeSelectedEvent(){this.selectedEvent=void 0,this.selectedEventIndex=void 0}getIndexOfKeyInMap(e){let A=0,i=(n,g)=>0,o=Array.from(this.eventData.keys()).sort(i);for(let n of o){if(n===e)return A;A++}}getKeyAtIndexInMap(e){let A=(o,n)=>0,i=Array.from(this.eventData.keys()).sort(A);if(e>=0&&e<i.length)return i[e]}openSnackBar(e,A){this._snackBar.open(e,A)}processThoughtText(e){return e.replace("/*PLANNING*/","").replace("/*ACTION*/","")}openLink(e){window.open(e,"_blank")}renderGooglerSearch(e){return this.sanitizer.bypassSecurityTrustHtml(e)}openViewImageDialog(e){let A=this.dialog.open(Gg,{data:{imageData:e}})}createDefaultArtifactName(e){return!e||!e.includes("/")?"":e.replace("/",".")}exportSession(){this.sessionService.getSession(this.userId,this.appName,this.sessionId).subscribe(e=>{console.log(e),this.downloadService.downloadObjectAsJson(e,`session-${this.sessionId}.json`)})}static \u0275fac=function(A){return new(A||t)(V(Vo),V(wo),V(ds),V(hs),V(yo),V(us),V(di),V(ms),V(Ii),V(Jn))};static \u0275cmp=O({type:t,selectors:[["app-chat"]],viewQuery:function(A,i){if(A&1&&(QA(fZ,5,q),QA(pZ,5),QA(Ug,5),QA(xg,5),QA(Kg,5),QA(wZ,5)),A&2){let o;$(o=AA())&&(i.videoContainer=o.first),$(o=AA())&&(i.sideDrawer=o.first),$(o=AA())&&(i.eventTabComponent=o.first),$(o=AA())&&(i.sessionTab=o.first),$(o=AA())&&(i.evalTab=o.first),$(o=AA())&&(i.scrollContainer=o.first)}},standalone:!1,features:[FA([{provide:Ng,useClass:FD}])],decls:27,vars:14,consts:[["sideDrawer",""],["autoScroll",""],["videoContainer",""],["fileInput",""],["autosize","",1,"drawer-container"],["matTooltip","Open panel",1,"material-symbols-outlined",2,"position","absolute","width","24px","height","24px","color","#C4C7C5","cursor","pointer","margin-left","20px","margin-top","20px"],["mode","side","appResizableDrawer","",1,"side-drawer"],[2,"margin-top","20px","margin-left","20px","display","flex"],[2,"width","100%"],[1,"drawer-header"],["matTooltip","Collapse panel",1,"material-symbols-outlined",2,"color","#C4C7C5","cursor","pointer",3,"click"],[1,"drawer-logo"],["src","assets/ADK-512-color.svg","width","32px","height","32px"],[1,"app-select-container"],[1,"app-select",3,"selectionChange","placeholder","formControl"],[3,"value"],[1,"tabs-container"],[1,"details-panel-container"],[1,"resize-handler"],[1,"chat-container"],[1,"chat-toolbar"],[1,"chat-card"],["mat-fab","","color","primary",1,"fab-button"],[1,"chat-messages"],[1,"chat-input"],["matTooltip","Open panel",1,"material-symbols-outlined",2,"position","absolute","width","24px","height","24px","color","#C4C7C5","cursor","pointer","margin-left","20px","margin-top","20px",3,"click"],[1,"tabs-header"],["mat-tab-label",""],[3,"selectedEvent","eventsMap","traceData"],[3,"sessionState"],[3,"artifacts"],[3,"sessionSelected","sessionReloaded","userId","appName","sessionId"],[1,"tab-label"],[3,"shouldShowTab","sessionSelected","appName","userId","sessionId"],[1,"details-content"],[2,"display","flex","justify-content","flex-end","margin-top","10px"],["aria-label","Select event",1,"event-paginator",3,"page","length","pageSize","pageIndex"],["mat-mini-fab",""],[3,"click"],["label","Event"],[1,"event-graph-container"],[3,"innerHtml"],[1,"json-viewer-container"],[3,"json"],["label","Request"],["label","Response"],[3,"click","innerHtml"],[2,"display","flex"],[1,"toolbar-session-text"],[1,"toolbar-session-id"],[1,"toolbar-actions"],[1,"toolbar-sse-toggle"],[1,"example-margin",3,"change","checked"],[2,"margin-left","8px","margin-right","8px","height","22px",3,"vertical"],[2,"display","flex","align-items","center"],[1,"toolbar-new-sesison",3,"click"],["matTooltip","Delete current session",1,"material-symbols-outlined",2,"width","24px","height","24px","color","#C4C7C5","cursor","pointer","margin-right","16px",3,"click"],[1,"material-symbols-outlined",2,"width","24px","height","24px","color","#C4C7C5","cursor","pointer","margin-right","16px",3,"click"],[1,"empty-state-container"],[1,"warning"],[1,"error"],["mat-fab","","color","primary",1,"fab-button",3,"click"],[3,"ngClass"],["mat-mini-fab","",3,"matTooltip"],[1,"message-card",3,"ngClass"],["mode","buffer",1,"loading-bar"],[1,"attachments"],[1,"thought-chip"],[1,"message-text",3,"data","ngStyle"],["mat-stroked-button","",1,"function-event-button"],[1,"tool-uses-container"],[1,"material-symbols-outlined"],["mat-mini-fab","",3,"click","matTooltip"],["fontSet","material-symbols-outlined"],[1,"attachment"],["alt","attachment",1,"image-preview-chat",3,"src"],["download","",3,"href"],[3,"innerHTML"],[1,"generated-image-container"],["alt","image",1,"generated-image",3,"click","src"],[3,"base64data"],[1,"html-artifact-container"],[1,"link-style-button",3,"click"],["alt","image",1,"image-preview-chat",3,"click","src"],["mat-stroked-button","",1,"function-event-button",3,"click"],[1,"actual-tool-uses"],[1,"tool-uses-header"],[1,"expected-tool-uses"],["type","file","multiple","","hidden","",3,"change"],["appearance","outline",1,"input-field"],[1,"file-preview"],["matInput","","cdkTextareaAutosize","","cdkAutosizeMinRows","1","cdkAutosizeMaxRows","10","placeholder","Type a Message...",1,"chat-input-box",2,"caret-color","white",3,"ngModelChange","keydown.enter","ngModel"],[1,"chat-input-actions"],["mat-icon-button","","matTooltip","Upload local file",1,"function-event-button",2,"margin-right","10px",3,"click"],["mat-icon-button","","matSuffix","",3,"click","ngStyle","matTooltip"],[1,"image-container"],[1,"file-container"],["alt","preview",1,"image-preview",3,"src"],["mat-icon-button","",1,"delete-button",3,"click"],["color","warn"],[1,"file-info"]],template:function(A,i){if(A&1){let o=rA();d(0,"mat-drawer-container",4),x(1,FZ,2,0,"span",5),d(2,"mat-drawer",6,0)(4,"div",7)(5,"div",8)(6,"div",9)(7,"span",10),G("click",function(){return Y(o),J(i.toggleSidePanel())}),k(8,"left_panel_close"),h(),d(9,"div",11),P(10,"img",12),k(11," Agent Development Kit "),h()()()(),d(12,"div",13)(13,"mat-select",14),G("selectionChange",function(g){return Y(o),J(i.onAppSelection(g))}),x(14,SZ,2,0),To(15,"async"),x(16,NZ,2,2,"mat-option",15),h()(),x(17,YZ,15,8,"div",16)(18,HZ,20,7,"div",17),P(19,"div",18),h(),d(20,"div",19),x(21,TZ,20,3,"div",20),d(22,"mat-card",21),x(23,zZ,2,1)(24,jZ,3,0,"button",22)(25,pq,6,0,"div",23)(26,kq,17,10,"div",24),h()()()}if(A&2){let o;D(),_(i.showSidePanel?-1:1),D(12),L("placeholder",i.isLoadingApps()?"Loading...":"Select an agent")("formControl",i.selectedAppControl),D(),_((o=br(15,12,i.apps$))?14:-1,o),D(2),_(i.selectedAppControl.value&&i.isLoadingApps()?16:-1),D(),_(i.appName!=""&&i.showSidePanel?17:-1),D(),_(i.selectedEvent&&i.showSidePanel?18:-1),D(3),_(i.appName!=""?21:-1),D(2),_(i.selectedAppControl.value?-1:23),D(),_(i.longRunningEvents.length>0?24:-1),D(),_(i.appName!=""?25:-1),D(),_(i.appName!=""?26:-1)}},dependencies:[zt,qh,ro,ai,jt,gF,Es,ho,Jk,Hn,Zb,Et,RE,mk,uk,_m,jb,ic,CD,BD,dD,hD,uF,Cs,Nn,Bs,fF,TF,ac,cu,Ug,xg,Kg,pI,xI,Lg,YI,fa],styles:[".expand-side-drawer[_ngcontent-%COMP%]{position:relative;top:4%;left:1%}.drawer-container[_ngcontent-%COMP%]{height:100%;background-color:#131314}.generated-image-container[_ngcontent-%COMP%]{max-width:400px}.generated-image[_ngcontent-%COMP%]{max-width:100%;border-radius:8px}.chat-container[_ngcontent-%COMP%]{width:100%;height:100%;max-width:1200px;margin:auto}.event-container[_ngcontent-%COMP%]{color:#fff}.html-artifact-container[_ngcontent-%COMP%], .drawer-header[_ngcontent-%COMP%]{width:100%;display:flex;justify-content:flex-start;align-items:center}.drawer-header[_ngcontent-%COMP%]   .mat-icon[_ngcontent-%COMP%]{width:36px;height:36px;color:#bdc1c6;cursor:pointer;display:flex;align-items:center;justify-content:center}.chat-card[_ngcontent-%COMP%]{display:flex;flex-direction:column;height:500px;overflow:hidden;height:95%;box-shadow:none;background-color:#131314}.loading-bar[_ngcontent-%COMP%]{width:100px;margin:15px}.chat-messages[_ngcontent-%COMP%]{flex-grow:1;overflow-y:auto;padding:20px;margin-top:16px}.message-card[_ngcontent-%COMP%]{padding:5px 20px;margin:5px;border-radius:20px;max-width:80%;font-size:14px;font-weight:400;position:relative;display:inline-block}.user-message[_ngcontent-%COMP%]{display:flex;justify-content:flex-end;align-items:center}.user-message[_ngcontent-%COMP%]   .message-card[_ngcontent-%COMP%]{background-color:#004a77;align-self:flex-end;color:#fff;box-shadow:none}.bot-message[_ngcontent-%COMP%]{display:flex;align-items:center}.bot-message[_ngcontent-%COMP%]   .message-card[_ngcontent-%COMP%]{background-color:#303030;align-self:flex-start;color:#fff;box-shadow:none}.message-card[_ngcontent-%COMP%]   .tool-uses-container[_ngcontent-%COMP%]{visibility:hidden;position:absolute;left:10px;z-index:10;display:flex;background-color:#484848;overflow:hidden;border-radius:20px;padding:5px 20px;margin-bottom:10px;font-size:16px}.message-card[_ngcontent-%COMP%]   .tool-uses-container[_ngcontent-%COMP%]   .actual-tool-uses[_ngcontent-%COMP%]{border-right:2px solid #8a8686;padding-right:8px}.message-card[_ngcontent-%COMP%]   .tool-uses-container[_ngcontent-%COMP%]   .expected-tool-uses[_ngcontent-%COMP%]{padding-left:12px}.message-card[_ngcontent-%COMP%]:hover   .tool-uses-container[_ngcontent-%COMP%]{visibility:visible}.tool-uses-header[_ngcontent-%COMP%]{padding-bottom:5px;border-bottom:2px solid #8a8686;font-style:italic;font-weight:700}.eval-pass[_ngcontent-%COMP%]{display:flex;color:#44c265}.eval-fail[_ngcontent-%COMP%]{display:flex;color:#ff8983}.navigation-button-sidepanel[_ngcontent-%COMP%]{margin-left:auto;margin-right:20px}.chat-input[_ngcontent-%COMP%]{display:flex;padding:10px;width:80%;margin:0 auto}.input-field[_ngcontent-%COMP%]{flex-grow:1}.input-field[_ngcontent-%COMP%]   textarea[_ngcontent-%COMP%]{color:#fff;border:none;padding:10px;box-sizing:content-box}.input-field[_ngcontent-%COMP%]   textarea[_ngcontent-%COMP%]::placeholder{color:#8e918f}.input-field[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{color:#fff;background-color:#333537}.chat-input-actions[_ngcontent-%COMP%]{margin-top:10px;display:flex;justify-content:space-between}.fab-button[_ngcontent-%COMP%]{position:fixed;bottom:200px;right:100px;z-index:1000}.sidepanel-toggle[_ngcontent-%COMP%]{position:relative;top:100px;z-index:1000}.side-drawer[_ngcontent-%COMP%]{background-color:#1b1b1b;color:#fff;border-radius:0}.tabs-container[_ngcontent-%COMP%]{width:100%;margin-top:20px}.tab-label[_ngcontent-%COMP%]{font-size:14px}.file-preview[_ngcontent-%COMP%]{display:flex;flex-wrap:wrap;gap:5px;margin-top:2px;margin-bottom:8px}.file-item[_ngcontent-%COMP%]{display:flex;align-items:center;gap:5px;background:#eee;padding:5px;border-radius:4px}.image-preview[_ngcontent-%COMP%]{width:40px;height:40px;object-fit:cover;border-radius:4px}.image-preview-chat[_ngcontent-%COMP%]{max-width:90%;max-height:70vh;width:auto;height:auto;border-radius:8px;cursor:pointer;transition:transform .2s ease-in-out}button[_ngcontent-%COMP%]{margin-left:20px;margin-right:20px}.app-select[_ngcontent-%COMP%]{width:180px}.empty-state-container[_ngcontent-%COMP%]{color:#eee;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;font-family:Open Sans,sans-serif;font-weight:400;letter-spacing:normal;line-height:24px;font-size:18px}.empty-state-container[_ngcontent-%COMP%]   pre.warning[_ngcontent-%COMP%]{color:#ffc185}.empty-state-container[_ngcontent-%COMP%]   pre.error[_ngcontent-%COMP%]{color:#ff4545}.function-event-button[_ngcontent-%COMP%]{background-color:#fff}[_nghost-%COMP%]     .message-text p{white-space:pre-line;word-break:break-word;overflow-wrap:break-word}[_nghost-%COMP%]     .mdc-linear-progress__buffer-dots{background:#fff}[_nghost-%COMP%]     .mat-mdc-text-field-wrapper{border:1px solid #8e918f}[_nghost-%COMP%]     .input-field .mat-mdc-text-field-wrapper{border:1px solid #8e918f;border-radius:16px}[_nghost-%COMP%]     .mdc-notched-outline__leading, [_nghost-%COMP%]     .mdc-notched-outline__notch, [_nghost-%COMP%]     .mdc-notched-outline__trailing{border:none}[_nghost-%COMP%]     .mat-mdc-form-field-icon-suffix{padding:0 10px 0 40px}[_nghost-%COMP%]     .segment-key{color:#d3d3d3!important}[_nghost-%COMP%]     .mat-mdc-mini-fab{background-color:#fff}[_nghost-%COMP%]     .mat-mdc-mini-fab mat-icon{color:#000}.mat-mdc-select-placeholder[_ngcontent-%COMP%]{margin-left:20px}.resize-handler[_ngcontent-%COMP%]{background:#5f6368;width:4px;border-radius:4px;position:absolute;display:block;height:20%;top:40%;right:0;z-index:9999;cursor:ew-resize}.new-session-button[_ngcontent-%COMP%]{margin-top:0;margin-left:50px;width:130px;height:28px;font-size:14px}.app-select-container[_ngcontent-%COMP%]{width:30%;margin-top:12px;background-color:#212123;margin-left:20px;height:30px;display:flex;justify-content:space-between;padding-left:20px;padding-right:20px;border-radius:10px;padding-top:5px}.app-select-container[_ngcontent-%COMP%]{--mat-select-placeholder-text-color: #8ab4f8}.app-select-container[_ngcontent-%COMP%]{--mat-select-enabled-trigger-text-color: #8ab4f8}.app-select-container[_ngcontent-%COMP%]{--mat-select-enabled-arrow-color: #8ab4f8}.json-viewer-container[_ngcontent-%COMP%]{margin:10px}.event-paginator[_ngcontent-%COMP%]{margin-top:-8px;margin-right:auto;background-color:inherit;display:flex;justify-content:center}[_nghost-%COMP%]     .mat-mdc-paginator-page-size{display:none!important}.details-panel-container[_ngcontent-%COMP%]{position:absolute;width:100%;height:98%;left:0;right:0;bottom:0;background:#242424;display:inline-block;justify-content:center;align-items:center;z-index:10}.details-content[_ngcontent-%COMP%]{color:#fff;font-size:14px}.adk-checkbox[_ngcontent-%COMP%]{position:fixed;bottom:0;left:0;right:0;margin-bottom:20px;margin-left:20px}.drawer-header[_ngcontent-%COMP%]{--mdc-filled-button-container-color: #89b4f8}.drawer-header[_ngcontent-%COMP%]{--mdc-filled-button-label-text-color: black}.chat-toolbar[_ngcontent-%COMP%]{position:sticky;top:0;height:48px;background:#1b1b1b;display:flex;justify-content:space-between;align-items:center;z-index:10}.toolbar-session-text[_ngcontent-%COMP%]{color:#fdfdfd;font-family:Roboto;font-size:12px;font-style:normal;font-weight:500;line-height:12px;letter-spacing:.8px;text-transform:uppercase;margin-left:20px;padding-top:4px}.toolbar-session-id[_ngcontent-%COMP%]{color:#9aa0a6;font-family:monospace;font-size:14px;font-style:normal;font-weight:400;line-height:20px;letter-spacing:.25px;margin-left:5px}.toolbar-actions[_ngcontent-%COMP%]{display:flex}.toolbar-new-sesison[_ngcontent-%COMP%]{font-size:14px;margin-right:16px;color:#9aa0a6;cursor:pointer;display:flex;align-items:center}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mat-switch-label-text-size: 14px}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mat-switch-label-text-color: #9aa0a6}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-selected-track-color: #8ab4f9}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-selected-focus-track-color: #8ab4f9}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-selected-hover-track-color: #8ab4f9}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-selected-handle-color: #1b73e8}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-selected-focus-handle-color: #1b73e8}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-selected-hover-handle-color: #1b73e8}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-track-height: 24px}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mdc-switch-track-width: 46px}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mat-switch-track-outline-color: #1b73e8}.toolbar-sse-toggle[_ngcontent-%COMP%]{--mat-switch-with-icon-handle-size: 20px}.image-container[_ngcontent-%COMP%]{position:relative;display:inline-block;border-radius:12px;overflow:hidden}.image-preview[_ngcontent-%COMP%]{display:block;width:100%;height:auto;border-radius:12px;width:80px;height:80px}.delete-button[_ngcontent-%COMP%]{position:absolute;top:1px;right:1px;background-color:#000000b3;border:none;border-radius:50%;padding:8px;cursor:pointer;color:#fff;display:flex;align-items:center;justify-content:center;margin-right:0;scale:.7}.delete-button[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:20px}.file-container[_ngcontent-%COMP%]{position:relative;display:flex;flex-direction:column;gap:8px;height:80px;background-color:#1e1e1e;border-radius:12px}.file-info[_ngcontent-%COMP%]{margin-right:60px;padding-top:20px;padding-left:16px}.thought-chip[_ngcontent-%COMP%]{border-radius:5px;background-color:#8ab4f8;width:80px;text-align:center;margin-top:5px}.event-graph-container[_ngcontent-%COMP%]{margin-top:16px;margin-bottom:16px;display:flex;justify-content:center;max-height:33%;cursor:pointer}.event-graph-container[_ngcontent-%COMP%]     svg{width:100%;height:100%;display:block;object-fit:contain}[_nghost-%COMP%]     pre{white-space:pre-wrap;word-break:break-word;overflow-x:auto;max-width:100%}.link-style-button[_ngcontent-%COMP%]{background:none;border:none;padding:0;font:inherit;color:#007bff!important;text-decoration:underline;cursor:pointer;outline:none;font-size:14px}.drawer-logo[_ngcontent-%COMP%]{margin-left:9px;display:flex;align-items:center;font-size:16px;font-style:normal;font-weight:500;line-height:24px;letter-spacing:.1px}.drawer-logo[_ngcontent-%COMP%]   img[_ngcontent-%COMP%]{margin-right:9px}"]})};var ps=class t{title="agent_framework_web";userId="";appName="";sessionId="";constructor(){}static \u0275fac=function(A){return new(A||t)};static \u0275cmp=O({type:t,selectors:[["app-root"]],standalone:!1,decls:1,vars:0,template:function(A,i){A&1&&P(0,"app-chat")},dependencies:[JI],encapsulation:2})};var vq=[{path:"",component:ps}],Ic=class t{static \u0275fac=function(A){return new(A||t)};static \u0275mod=X({type:t});static \u0275inj=j({imports:[oE.forRoot(vq),oE]})};function VF(t){return new H(3e3,!1)}function Sq(){return new H(3100,!1)}function Nq(){return new H(3101,!1)}function Gq(t){return new H(3001,!1)}function Lq(t){return new H(3003,!1)}function _q(t){return new H(3004,!1)}function zF(t,e){return new H(3005,!1)}function jF(){return new H(3006,!1)}function XF(){return new H(3007,!1)}function $F(t,e){return new H(3008,!1)}function Av(t){return new H(3002,!1)}function ev(t,e,A,i,o){return new H(3010,!1)}function tv(){return new H(3011,!1)}function iv(){return new H(3012,!1)}function ov(){return new H(3200,!1)}function nv(){return new H(3202,!1)}function gv(){return new H(3013,!1)}function rv(t){return new H(3014,!1)}function sv(t){return new H(3015,!1)}function av(t){return new H(3016,!1)}function Iv(t,e){return new H(3404,!1)}function Kq(t){return new H(3502,!1)}function Cv(t){return new H(3503,!1)}function Bv(){return new H(3300,!1)}function Qv(t){return new H(3504,!1)}function Ev(t){return new H(3301,!1)}function cv(t,e){return new H(3302,!1)}function lv(t){return new H(3303,!1)}function dv(t,e){return new H(3400,!1)}function hv(t){return new H(3401,!1)}function uv(t){return new H(3402,!1)}function mv(t,e){return new H(3505,!1)}function nn(t){switch(t.length){case 0:return new co;case 1:return t[0];default:return new Sg(t)}}function GD(t,e,A=new Map,i=new Map){let o=[],n=[],g=-1,r=null;if(e.forEach(s=>{let a=s.get("offset"),Q=a==g,c=Q&&r||new Map;s.forEach((f,m)=>{let p=m,M=f;if(m!=="offset")switch(p=t.normalizePropertyName(p,o),M){case Is:M=A.get(m);break;case ci:M=i.get(m);break;default:M=t.normalizeStyleValue(m,p,M,o);break}c.set(p,M)}),Q||n.push(c),r=c,g=a}),o.length)throw Kq(o);return n}function Cc(t,e,A,i){switch(e){case"start":t.onStart(()=>i(A&&vD(A,"start",t)));break;case"done":t.onDone(()=>i(A&&vD(A,"done",t)));break;case"destroy":t.onDestroy(()=>i(A&&vD(A,"destroy",t)));break}}function vD(t,e,A){let i=A.totalTime,o=!!A.disabled,n=Bc(t.element,t.triggerName,t.fromState,t.toState,e||t.phaseName,i??t.totalTime,o),g=t._data;return g!=null&&(n._data=g),n}function Bc(t,e,A,i,o="",n=0,g){return{element:t,triggerName:e,fromState:A,toState:i,phaseName:o,totalTime:n,disabled:!!g}}function Yt(t,e,A){let i=t.get(e);return i||t.set(e,i=A),i}function LD(t){let e=t.indexOf(":"),A=t.substring(1,e),i=t.slice(e+1);return[A,i]}var Uq=typeof document>"u"?null:document.documentElement;function Qc(t){let e=t.parentNode||t.host||null;return e===Uq?null:e}function xq(t){return t.substring(1,6)=="ebkit"}var Hg=null,WF=!1;function Dv(t){Hg||(Hg=Yq()||{},WF=Hg.style?"WebkitAppearance"in Hg.style:!1);let e=!0;return Hg.style&&!xq(t)&&(e=t in Hg.style,!e&&WF&&(e="Webkit"+t.charAt(0).toUpperCase()+t.slice(1)in Hg.style)),e}function Yq(){return typeof document<"u"?document.body:null}function _D(t,e){for(;e;){if(e===t)return!0;e=Qc(e)}return!1}function KD(t,e,A){if(A)return Array.from(t.querySelectorAll(e));let i=t.querySelector(e);return i?[i]:[]}var Jq=1e3,UD="{{",Hq="}}",xD="ng-enter",Ec="ng-leave",HI="ng-trigger",TI=".ng-trigger",YD="ng-animating",cc=".ng-animating";function ko(t){if(typeof t=="number")return t;let e=t.match(/^(-?[\.\d]+)(m?s)/);return!e||e.length<2?0:SD(parseFloat(e[1]),e[2])}function SD(t,e){switch(e){case"s":return t*Jq;default:return t}}function OI(t,e,A){return t.hasOwnProperty("duration")?t:Tq(t,e,A)}function Tq(t,e,A){let i=/^(-?[\.\d]+)(m?s)(?:\s+(-?[\.\d]+)(m?s))?(?:\s+([-a-z]+(?:\(.+?\))?))?$/i,o,n=0,g="";if(typeof t=="string"){let r=t.match(i);if(r===null)return e.push(VF(t)),{duration:0,delay:0,easing:""};o=SD(parseFloat(r[1]),r[2]);let s=r[3];s!=null&&(n=SD(parseFloat(s),r[4]));let a=r[5];a&&(g=a)}else o=t;if(!A){let r=!1,s=e.length;o<0&&(e.push(Sq()),r=!0),n<0&&(e.push(Nq()),r=!0),r&&e.splice(s,0,VF(t))}return{duration:o,delay:n,easing:g}}function fv(t){return t.length?t[0]instanceof Map?t:t.map(e=>new Map(Object.entries(e))):[]}function Yi(t,e,A){e.forEach((i,o)=>{let n=lc(o);A&&!A.has(o)&&A.set(o,t.style[n]),t.style[n]=i})}function Tn(t,e){e.forEach((A,i)=>{let o=lc(i);t.style[o]=""})}function ws(t){return Array.isArray(t)?t.length==1?t[0]:Sk(t):t}function pv(t,e,A){let i=e.params||{},o=JD(t);o.length&&o.forEach(n=>{i.hasOwnProperty(n)||A.push(Gq(n))})}var ND=new RegExp(`${UD}\\s*(.+?)\\s*${Hq}`,"g");function JD(t){let e=[];if(typeof t=="string"){let A;for(;A=ND.exec(t);)e.push(A[1]);ND.lastIndex=0}return e}function ys(t,e,A){let i=`${t}`,o=i.replace(ND,(n,g)=>{let r=e[g];return r==null&&(A.push(Lq(g)),r=""),r.toString()});return o==i?t:o}var Oq=/-+([a-z0-9])/g;function lc(t){return t.replace(Oq,(...e)=>e[1].toUpperCase())}function wv(t,e){return t===0||e===0}function yv(t,e,A){if(A.size&&e.length){let i=e[0],o=[];if(A.forEach((n,g)=>{i.has(g)||o.push(g),i.set(g,n)}),o.length)for(let n=1;n<e.length;n++){let g=e[n];o.forEach(r=>g.set(r,dc(t,r)))}}return e}function Jt(t,e,A){switch(e.type){case UA.Trigger:return t.visitTrigger(e,A);case UA.State:return t.visitState(e,A);case UA.Transition:return t.visitTransition(e,A);case UA.Sequence:return t.visitSequence(e,A);case UA.Group:return t.visitGroup(e,A);case UA.Animate:return t.visitAnimate(e,A);case UA.Keyframes:return t.visitKeyframes(e,A);case UA.Style:return t.visitStyle(e,A);case UA.Reference:return t.visitReference(e,A);case UA.AnimateChild:return t.visitAnimateChild(e,A);case UA.AnimateRef:return t.visitAnimateRef(e,A);case UA.Query:return t.visitQuery(e,A);case UA.Stagger:return t.visitStagger(e,A);default:throw _q(e.type)}}function dc(t,e){return window.getComputedStyle(t)[e]}var nf=(()=>{class t{validateStyleProperty(A){return Dv(A)}containsElement(A,i){return _D(A,i)}getParentElement(A){return Qc(A)}query(A,i,o){return KD(A,i,o)}computeStyle(A,i,o){return o||""}animate(A,i,o,n,g,r=[],s){return new co(o,n)}static \u0275fac=function(i){return new(i||t)};static \u0275prov=S({token:t,factory:t.\u0275fac})}return t})(),Og=class{static NOOP=new nf},Pg=class{};var Pq=new Set(["width","height","minWidth","minHeight","maxWidth","maxHeight","left","top","bottom","right","fontSize","outlineWidth","outlineOffset","paddingTop","paddingLeft","paddingBottom","paddingRight","marginTop","marginLeft","marginBottom","marginRight","borderRadius","borderWidth","borderTopWidth","borderLeftWidth","borderRightWidth","borderBottomWidth","textIndent","perspective"]),fc=class extends Pg{normalizePropertyName(e,A){return lc(e)}normalizeStyleValue(e,A,i,o){let n="",g=i.toString().trim();if(Pq.has(A)&&i!==0&&i!=="0")if(typeof i=="number")n="px";else{let r=i.match(/^[+-]?[\d\.]+([a-z]*)$/);r&&r[1].length==0&&o.push(zF(e,i))}return g+n}};var pc="*";function Zq(t,e){let A=[];return typeof t=="string"?t.split(/\s*,\s*/).forEach(i=>qq(i,A,e)):A.push(t),A}function qq(t,e,A){if(t[0]==":"){let s=Vq(t,A);if(typeof s=="function"){e.push(s);return}t=s}let i=t.match(/^(\*|[-\w]+)\s*(<?[=-]>)\s*(\*|[-\w]+)$/);if(i==null||i.length<4)return A.push(sv(t)),e;let o=i[1],n=i[2],g=i[3];e.push(Mv(o,g));let r=o==pc&&g==pc;n[0]=="<"&&!r&&e.push(Mv(g,o))}function Vq(t,e){switch(t){case":enter":return"void => *";case":leave":return"* => void";case":increment":return(A,i)=>parseFloat(i)>parseFloat(A);case":decrement":return(A,i)=>parseFloat(i)<parseFloat(A);default:return e.push(av(t)),"* => *"}}var hc=new Set(["true","1"]),uc=new Set(["false","0"]);function Mv(t,e){let A=hc.has(t)||uc.has(t),i=hc.has(e)||uc.has(e);return(o,n)=>{let g=t==pc||t==o,r=e==pc||e==n;return!g&&A&&typeof o=="boolean"&&(g=o?hc.has(t):uc.has(t)),!r&&i&&typeof n=="boolean"&&(r=n?hc.has(e):uc.has(e)),g&&r}}var _v=":self",Wq=new RegExp(`s*${_v}s*,?`,"g");function Kv(t,e,A,i){return new qD(t).build(e,A,i)}var Rv="",qD=class{_driver;constructor(e){this._driver=e}build(e,A,i){let o=new VD(A);return this._resetContextStyleTimingState(o),Jt(this,ws(e),o)}_resetContextStyleTimingState(e){e.currentQuerySelector=Rv,e.collectedStyles=new Map,e.collectedStyles.set(Rv,new Map),e.currentTime=0}visitTrigger(e,A){let i=A.queryCount=0,o=A.depCount=0,n=[],g=[];return e.name.charAt(0)=="@"&&A.errors.push(jF()),e.definitions.forEach(r=>{if(this._resetContextStyleTimingState(A),r.type==UA.State){let s=r,a=s.name;a.toString().split(/\s*,\s*/).forEach(Q=>{s.name=Q,n.push(this.visitState(s,A))}),s.name=a}else if(r.type==UA.Transition){let s=this.visitTransition(r,A);i+=s.queryCount,o+=s.depCount,g.push(s)}else A.errors.push(XF())}),{type:UA.Trigger,name:e.name,states:n,transitions:g,queryCount:i,depCount:o,options:null}}visitState(e,A){let i=this.visitStyle(e.styles,A),o=e.options&&e.options.params||null;if(i.containsDynamicStyles){let n=new Set,g=o||{};i.styles.forEach(r=>{r instanceof Map&&r.forEach(s=>{JD(s).forEach(a=>{g.hasOwnProperty(a)||n.add(a)})})}),n.size&&A.errors.push($F(e.name,[...n.values()]))}return{type:UA.State,name:e.name,style:i,options:o?{params:o}:null}}visitTransition(e,A){A.queryCount=0,A.depCount=0;let i=Jt(this,ws(e.animation),A),o=Zq(e.expr,A.errors);return{type:UA.Transition,matchers:o,animation:i,queryCount:A.queryCount,depCount:A.depCount,options:Tg(e.options)}}visitSequence(e,A){return{type:UA.Sequence,steps:e.steps.map(i=>Jt(this,i,A)),options:Tg(e.options)}}visitGroup(e,A){let i=A.currentTime,o=0,n=e.steps.map(g=>{A.currentTime=i;let r=Jt(this,g,A);return o=Math.max(o,A.currentTime),r});return A.currentTime=o,{type:UA.Group,steps:n,options:Tg(e.options)}}visitAnimate(e,A){let i=$q(e.timings,A.errors);A.currentAnimateTimings=i;let o,n=e.styles?e.styles:Ue({});if(n.type==UA.Keyframes)o=this.visitKeyframes(n,A);else{let g=e.styles,r=!1;if(!g){r=!0;let a={};i.easing&&(a.easing=i.easing),g=Ue(a)}A.currentTime+=i.duration+i.delay;let s=this.visitStyle(g,A);s.isEmptyStep=r,o=s}return A.currentAnimateTimings=null,{type:UA.Animate,timings:i,style:o,options:null}}visitStyle(e,A){let i=this._makeStyleAst(e,A);return this._validateStyleAst(i,A),i}_makeStyleAst(e,A){let i=[],o=Array.isArray(e.styles)?e.styles:[e.styles];for(let r of o)typeof r=="string"?r===ci?i.push(r):A.errors.push(Av(r)):i.push(new Map(Object.entries(r)));let n=!1,g=null;return i.forEach(r=>{if(r instanceof Map&&(r.has("easing")&&(g=r.get("easing"),r.delete("easing")),!n)){for(let s of r.values())if(s.toString().indexOf(UD)>=0){n=!0;break}}}),{type:UA.Style,styles:i,easing:g,offset:e.offset,containsDynamicStyles:n,options:null}}_validateStyleAst(e,A){let i=A.currentAnimateTimings,o=A.currentTime,n=A.currentTime;i&&n>0&&(n-=i.duration+i.delay),e.styles.forEach(g=>{typeof g!="string"&&g.forEach((r,s)=>{let a=A.collectedStyles.get(A.currentQuerySelector),Q=a.get(s),c=!0;Q&&(n!=o&&n>=Q.startTime&&o<=Q.endTime&&(A.errors.push(ev(s,Q.startTime,Q.endTime,n,o)),c=!1),n=Q.startTime),c&&a.set(s,{startTime:n,endTime:o}),A.options&&pv(r,A.options,A.errors)})})}visitKeyframes(e,A){let i={type:UA.Keyframes,styles:[],options:null};if(!A.currentAnimateTimings)return A.errors.push(tv()),i;let o=1,n=0,g=[],r=!1,s=!1,a=0,Q=e.steps.map(W=>{let DA=this._makeStyleAst(W,A),xA=DA.offset!=null?DA.offset:Xq(DA.styles),wA=0;return xA!=null&&(n++,wA=DA.offset=xA),s=s||wA<0||wA>1,r=r||wA<a,a=wA,g.push(wA),DA});s&&A.errors.push(iv()),r&&A.errors.push(ov());let c=e.steps.length,f=0;n>0&&n<c?A.errors.push(nv()):n==0&&(f=o/(c-1));let m=c-1,p=A.currentTime,M=A.currentAnimateTimings,K=M.duration;return Q.forEach((W,DA)=>{let xA=f>0?DA==m?1:f*DA:g[DA],wA=xA*K;A.currentTime=p+M.delay+wA,M.duration=wA,this._validateStyleAst(W,A),W.offset=xA,i.styles.push(W)}),i}visitReference(e,A){return{type:UA.Reference,animation:Jt(this,ws(e.animation),A),options:Tg(e.options)}}visitAnimateChild(e,A){return A.depCount++,{type:UA.AnimateChild,options:Tg(e.options)}}visitAnimateRef(e,A){return{type:UA.AnimateRef,animation:this.visitReference(e.animation,A),options:Tg(e.options)}}visitQuery(e,A){let i=A.currentQuerySelector,o=e.options||{};A.queryCount++,A.currentQuery=e;let[n,g]=zq(e.selector);A.currentQuerySelector=i.length?i+" "+n:n,Yt(A.collectedStyles,A.currentQuerySelector,new Map);let r=Jt(this,ws(e.animation),A);return A.currentQuery=null,A.currentQuerySelector=i,{type:UA.Query,selector:n,limit:o.limit||0,optional:!!o.optional,includeSelf:g,animation:r,originalSelector:e.selector,options:Tg(e.options)}}visitStagger(e,A){A.currentQuery||A.errors.push(gv());let i=e.timings==="full"?{duration:0,delay:0,easing:"full"}:OI(e.timings,A.errors,!0);return{type:UA.Stagger,animation:Jt(this,ws(e.animation),A),timings:i,options:null}}};function zq(t){let e=!!t.split(/\s*,\s*/).find(A=>A==_v);return e&&(t=t.replace(Wq,"")),t=t.replace(/@\*/g,TI).replace(/@\w+/g,A=>TI+"-"+A.slice(1)).replace(/:animating/g,cc),[t,e]}function jq(t){return t?b({},t):null}var VD=class{errors;queryCount=0;depCount=0;currentTransition=null;currentQuery=null;currentQuerySelector=null;currentAnimateTimings=null;currentTime=0;collectedStyles=new Map;options=null;unsupportedCSSPropertiesFound=new Set;constructor(e){this.errors=e}};function Xq(t){if(typeof t=="string")return null;let e=null;if(Array.isArray(t))t.forEach(A=>{if(A instanceof Map&&A.has("offset")){let i=A;e=parseFloat(i.get("offset")),i.delete("offset")}});else if(t instanceof Map&&t.has("offset")){let A=t;e=parseFloat(A.get("offset")),A.delete("offset")}return e}function $q(t,e){if(t.hasOwnProperty("duration"))return t;if(typeof t=="number"){let n=OI(t,e).duration;return HD(n,0,"")}let A=t;if(A.split(/\s+/).some(n=>n.charAt(0)=="{"&&n.charAt(1)=="{")){let n=HD(0,0,"");return n.dynamic=!0,n.strValue=A,n}let o=OI(A,e);return HD(o.duration,o.delay,o.easing)}function Tg(t){return t?(t=b({},t),t.params&&(t.params=jq(t.params))):t={},t}function HD(t,e,A){return{duration:t,delay:e,easing:A}}function gf(t,e,A,i,o,n,g=null,r=!1){return{type:1,element:t,keyframes:e,preStyleProps:A,postStyleProps:i,duration:o,delay:n,totalTime:o+n,easing:g,subTimeline:r}}var ZI=class{_map=new Map;get(e){return this._map.get(e)||[]}append(e,A){let i=this._map.get(e);i||this._map.set(e,i=[]),i.push(...A)}has(e){return this._map.has(e)}clear(){this._map.clear()}},AV=1,eV=":enter",tV=new RegExp(eV,"g"),iV=":leave",oV=new RegExp(iV,"g");function Uv(t,e,A,i,o,n=new Map,g=new Map,r,s,a=[]){return new WD().buildKeyframes(t,e,A,i,o,n,g,r,s,a)}var WD=class{buildKeyframes(e,A,i,o,n,g,r,s,a,Q=[]){a=a||new ZI;let c=new zD(e,A,a,o,n,Q,[]);c.options=s;let f=s.delay?ko(s.delay):0;c.currentTimeline.delayNextStep(f),c.currentTimeline.setStyles([g],null,c.errors,s),Jt(this,i,c);let m=c.timelines.filter(p=>p.containsAnimation());if(m.length&&r.size){let p;for(let M=m.length-1;M>=0;M--){let K=m[M];if(K.element===A){p=K;break}}p&&!p.allowOnlyTimelineStyles()&&p.setStyles([r],null,c.errors,s)}return m.length?m.map(p=>p.buildKeyframes()):[gf(A,[],[],[],0,f,"",!1)]}visitTrigger(e,A){}visitState(e,A){}visitTransition(e,A){}visitAnimateChild(e,A){let i=A.subInstructions.get(A.element);if(i){let o=A.createSubContext(e.options),n=A.currentTimeline.currentTime,g=this._visitSubInstructions(i,o,o.options);n!=g&&A.transformIntoNewTimeline(g)}A.previousNode=e}visitAnimateRef(e,A){let i=A.createSubContext(e.options);i.transformIntoNewTimeline(),this._applyAnimationRefDelays([e.options,e.animation.options],A,i),this.visitReference(e.animation,i),A.transformIntoNewTimeline(i.currentTimeline.currentTime),A.previousNode=e}_applyAnimationRefDelays(e,A,i){for(let o of e){let n=o?.delay;if(n){let g=typeof n=="number"?n:ko(ys(n,o?.params??{},A.errors));i.delayNextStep(g)}}}_visitSubInstructions(e,A,i){let n=A.currentTimeline.currentTime,g=i.duration!=null?ko(i.duration):null,r=i.delay!=null?ko(i.delay):null;return g!==0&&e.forEach(s=>{let a=A.appendInstructionToTimeline(s,g,r);n=Math.max(n,a.duration+a.delay)}),n}visitReference(e,A){A.updateOptions(e.options,!0),Jt(this,e.animation,A),A.previousNode=e}visitSequence(e,A){let i=A.subContextCount,o=A,n=e.options;if(n&&(n.params||n.delay)&&(o=A.createSubContext(n),o.transformIntoNewTimeline(),n.delay!=null)){o.previousNode.type==UA.Style&&(o.currentTimeline.snapshotCurrentStyles(),o.previousNode=wc);let g=ko(n.delay);o.delayNextStep(g)}e.steps.length&&(e.steps.forEach(g=>Jt(this,g,o)),o.currentTimeline.applyStylesToKeyframe(),o.subContextCount>i&&o.transformIntoNewTimeline()),A.previousNode=e}visitGroup(e,A){let i=[],o=A.currentTimeline.currentTime,n=e.options&&e.options.delay?ko(e.options.delay):0;e.steps.forEach(g=>{let r=A.createSubContext(e.options);n&&r.delayNextStep(n),Jt(this,g,r),o=Math.max(o,r.currentTimeline.currentTime),i.push(r.currentTimeline)}),i.forEach(g=>A.currentTimeline.mergeTimelineCollectedStyles(g)),A.transformIntoNewTimeline(o),A.previousNode=e}_visitTiming(e,A){if(e.dynamic){let i=e.strValue,o=A.params?ys(i,A.params,A.errors):i;return OI(o,A.errors)}else return{duration:e.duration,delay:e.delay,easing:e.easing}}visitAnimate(e,A){let i=A.currentAnimateTimings=this._visitTiming(e.timings,A),o=A.currentTimeline;i.delay&&(A.incrementTime(i.delay),o.snapshotCurrentStyles());let n=e.style;n.type==UA.Keyframes?this.visitKeyframes(n,A):(A.incrementTime(i.duration),this.visitStyle(n,A),o.applyStylesToKeyframe()),A.currentAnimateTimings=null,A.previousNode=e}visitStyle(e,A){let i=A.currentTimeline,o=A.currentAnimateTimings;!o&&i.hasCurrentStyleProperties()&&i.forwardFrame();let n=o&&o.easing||e.easing;e.isEmptyStep?i.applyEmptyStep(n):i.setStyles(e.styles,n,A.errors,A.options),A.previousNode=e}visitKeyframes(e,A){let i=A.currentAnimateTimings,o=A.currentTimeline.duration,n=i.duration,r=A.createSubContext().currentTimeline;r.easing=i.easing,e.styles.forEach(s=>{let a=s.offset||0;r.forwardTime(a*n),r.setStyles(s.styles,s.easing,A.errors,A.options),r.applyStylesToKeyframe()}),A.currentTimeline.mergeTimelineCollectedStyles(r),A.transformIntoNewTimeline(o+n),A.previousNode=e}visitQuery(e,A){let i=A.currentTimeline.currentTime,o=e.options||{},n=o.delay?ko(o.delay):0;n&&(A.previousNode.type===UA.Style||i==0&&A.currentTimeline.hasCurrentStyleProperties())&&(A.currentTimeline.snapshotCurrentStyles(),A.previousNode=wc);let g=i,r=A.invokeQuery(e.selector,e.originalSelector,e.limit,e.includeSelf,!!o.optional,A.errors);A.currentQueryTotal=r.length;let s=null;r.forEach((a,Q)=>{A.currentQueryIndex=Q;let c=A.createSubContext(e.options,a);n&&c.delayNextStep(n),a===A.element&&(s=c.currentTimeline),Jt(this,e.animation,c),c.currentTimeline.applyStylesToKeyframe();let f=c.currentTimeline.currentTime;g=Math.max(g,f)}),A.currentQueryIndex=0,A.currentQueryTotal=0,A.transformIntoNewTimeline(g),s&&(A.currentTimeline.mergeTimelineCollectedStyles(s),A.currentTimeline.snapshotCurrentStyles()),A.previousNode=e}visitStagger(e,A){let i=A.parentContext,o=A.currentTimeline,n=e.timings,g=Math.abs(n.duration),r=g*(A.currentQueryTotal-1),s=g*A.currentQueryIndex;switch(n.duration<0?"reverse":n.easing){case"reverse":s=r-s;break;case"full":s=i.currentStaggerTime;break}let Q=A.currentTimeline;s&&Q.delayNextStep(s);let c=Q.currentTime;Jt(this,e.animation,A),A.previousNode=e,i.currentStaggerTime=o.currentTime-c+(o.startTime-i.currentTimeline.startTime)}},wc={},zD=class t{_driver;element;subInstructions;_enterClassName;_leaveClassName;errors;timelines;parentContext=null;currentTimeline;currentAnimateTimings=null;previousNode=wc;subContextCount=0;options={};currentQueryIndex=0;currentQueryTotal=0;currentStaggerTime=0;constructor(e,A,i,o,n,g,r,s){this._driver=e,this.element=A,this.subInstructions=i,this._enterClassName=o,this._leaveClassName=n,this.errors=g,this.timelines=r,this.currentTimeline=s||new yc(this._driver,A,0),r.push(this.currentTimeline)}get params(){return this.options.params}updateOptions(e,A){if(!e)return;let i=e,o=this.options;i.duration!=null&&(o.duration=ko(i.duration)),i.delay!=null&&(o.delay=ko(i.delay));let n=i.params;if(n){let g=o.params;g||(g=this.options.params={}),Object.keys(n).forEach(r=>{(!A||!g.hasOwnProperty(r))&&(g[r]=ys(n[r],g,this.errors))})}}_copyOptions(){let e={};if(this.options){let A=this.options.params;if(A){let i=e.params={};Object.keys(A).forEach(o=>{i[o]=A[o]})}}return e}createSubContext(e=null,A,i){let o=A||this.element,n=new t(this._driver,o,this.subInstructions,this._enterClassName,this._leaveClassName,this.errors,this.timelines,this.currentTimeline.fork(o,i||0));return n.previousNode=this.previousNode,n.currentAnimateTimings=this.currentAnimateTimings,n.options=this._copyOptions(),n.updateOptions(e),n.currentQueryIndex=this.currentQueryIndex,n.currentQueryTotal=this.currentQueryTotal,n.parentContext=this,this.subContextCount++,n}transformIntoNewTimeline(e){return this.previousNode=wc,this.currentTimeline=this.currentTimeline.fork(this.element,e),this.timelines.push(this.currentTimeline),this.currentTimeline}appendInstructionToTimeline(e,A,i){let o={duration:A??e.duration,delay:this.currentTimeline.currentTime+(i??0)+e.delay,easing:""},n=new jD(this._driver,e.element,e.keyframes,e.preStyleProps,e.postStyleProps,o,e.stretchStartingKeyframe);return this.timelines.push(n),o}incrementTime(e){this.currentTimeline.forwardTime(this.currentTimeline.duration+e)}delayNextStep(e){e>0&&this.currentTimeline.delayNextStep(e)}invokeQuery(e,A,i,o,n,g){let r=[];if(o&&r.push(this.element),e.length>0){e=e.replace(tV,"."+this._enterClassName),e=e.replace(oV,"."+this._leaveClassName);let s=i!=1,a=this._driver.query(this.element,e,s);i!==0&&(a=i<0?a.slice(a.length+i,a.length):a.slice(0,i)),r.push(...a)}return!n&&r.length==0&&g.push(rv(A)),r}},yc=class t{_driver;element;startTime;_elementTimelineStylesLookup;duration=0;easing=null;_previousKeyframe=new Map;_currentKeyframe=new Map;_keyframes=new Map;_styleSummary=new Map;_localTimelineStyles=new Map;_globalTimelineStyles;_pendingStyles=new Map;_backFill=new Map;_currentEmptyStepKeyframe=null;constructor(e,A,i,o){this._driver=e,this.element=A,this.startTime=i,this._elementTimelineStylesLookup=o,this._elementTimelineStylesLookup||(this._elementTimelineStylesLookup=new Map),this._globalTimelineStyles=this._elementTimelineStylesLookup.get(A),this._globalTimelineStyles||(this._globalTimelineStyles=this._localTimelineStyles,this._elementTimelineStylesLookup.set(A,this._localTimelineStyles)),this._loadKeyframe()}containsAnimation(){switch(this._keyframes.size){case 0:return!1;case 1:return this.hasCurrentStyleProperties();default:return!0}}hasCurrentStyleProperties(){return this._currentKeyframe.size>0}get currentTime(){return this.startTime+this.duration}delayNextStep(e){let A=this._keyframes.size===1&&this._pendingStyles.size;this.duration||A?(this.forwardTime(this.currentTime+e),A&&this.snapshotCurrentStyles()):this.startTime+=e}fork(e,A){return this.applyStylesToKeyframe(),new t(this._driver,e,A||this.currentTime,this._elementTimelineStylesLookup)}_loadKeyframe(){this._currentKeyframe&&(this._previousKeyframe=this._currentKeyframe),this._currentKeyframe=this._keyframes.get(this.duration),this._currentKeyframe||(this._currentKeyframe=new Map,this._keyframes.set(this.duration,this._currentKeyframe))}forwardFrame(){this.duration+=AV,this._loadKeyframe()}forwardTime(e){this.applyStylesToKeyframe(),this.duration=e,this._loadKeyframe()}_updateStyle(e,A){this._localTimelineStyles.set(e,A),this._globalTimelineStyles.set(e,A),this._styleSummary.set(e,{time:this.currentTime,value:A})}allowOnlyTimelineStyles(){return this._currentEmptyStepKeyframe!==this._currentKeyframe}applyEmptyStep(e){e&&this._previousKeyframe.set("easing",e);for(let[A,i]of this._globalTimelineStyles)this._backFill.set(A,i||ci),this._currentKeyframe.set(A,ci);this._currentEmptyStepKeyframe=this._currentKeyframe}setStyles(e,A,i,o){A&&this._previousKeyframe.set("easing",A);let n=o&&o.params||{},g=nV(e,this._globalTimelineStyles);for(let[r,s]of g){let a=ys(s,n,i);this._pendingStyles.set(r,a),this._localTimelineStyles.has(r)||this._backFill.set(r,this._globalTimelineStyles.get(r)??ci),this._updateStyle(r,a)}}applyStylesToKeyframe(){this._pendingStyles.size!=0&&(this._pendingStyles.forEach((e,A)=>{this._currentKeyframe.set(A,e)}),this._pendingStyles.clear(),this._localTimelineStyles.forEach((e,A)=>{this._currentKeyframe.has(A)||this._currentKeyframe.set(A,e)}))}snapshotCurrentStyles(){for(let[e,A]of this._localTimelineStyles)this._pendingStyles.set(e,A),this._updateStyle(e,A)}getFinalKeyframe(){return this._keyframes.get(this.duration)}get properties(){let e=[];for(let A in this._currentKeyframe)e.push(A);return e}mergeTimelineCollectedStyles(e){e._styleSummary.forEach((A,i)=>{let o=this._styleSummary.get(i);(!o||A.time>o.time)&&this._updateStyle(i,A.value)})}buildKeyframes(){this.applyStylesToKeyframe();let e=new Set,A=new Set,i=this._keyframes.size===1&&this.duration===0,o=[];this._keyframes.forEach((r,s)=>{let a=new Map([...this._backFill,...r]);a.forEach((Q,c)=>{Q===Is?e.add(c):Q===ci&&A.add(c)}),i||a.set("offset",s/this.duration),o.push(a)});let n=[...e.values()],g=[...A.values()];if(i){let r=o[0],s=new Map(r);r.set("offset",0),s.set("offset",1),o=[r,s]}return gf(this.element,o,n,g,this.duration,this.startTime,this.easing,!1)}},jD=class extends yc{keyframes;preStyleProps;postStyleProps;_stretchStartingKeyframe;timings;constructor(e,A,i,o,n,g,r=!1){super(e,A,g.delay),this.keyframes=i,this.preStyleProps=o,this.postStyleProps=n,this._stretchStartingKeyframe=r,this.timings={duration:g.duration,delay:g.delay,easing:g.easing}}containsAnimation(){return this.keyframes.length>1}buildKeyframes(){let e=this.keyframes,{delay:A,duration:i,easing:o}=this.timings;if(this._stretchStartingKeyframe&&A){let n=[],g=i+A,r=A/g,s=new Map(e[0]);s.set("offset",0),n.push(s);let a=new Map(e[0]);a.set("offset",kv(r)),n.push(a);let Q=e.length-1;for(let c=1;c<=Q;c++){let f=new Map(e[c]),m=f.get("offset"),p=A+m*i;f.set("offset",kv(p/g)),n.push(f)}i=g,A=0,o="",e=n}return gf(this.element,e,this.preStyleProps,this.postStyleProps,i,A,o,!0)}};function kv(t,e=3){let A=Math.pow(10,e-1);return Math.round(t*A)/A}function nV(t,e){let A=new Map,i;return t.forEach(o=>{if(o==="*"){i??=e.keys();for(let n of i)A.set(n,ci)}else for(let[n,g]of o)A.set(n,g)}),A}function bv(t,e,A,i,o,n,g,r,s,a,Q,c,f){return{type:0,element:t,triggerName:e,isRemovalTransition:o,fromState:A,fromStyles:n,toState:i,toStyles:g,timelines:r,queriedElements:s,preStyleProps:a,postStyleProps:Q,totalTime:c,errors:f}}var TD={},Mc=class{_triggerName;ast;_stateStyles;constructor(e,A,i){this._triggerName=e,this.ast=A,this._stateStyles=i}match(e,A,i,o){return gV(this.ast.matchers,e,A,i,o)}buildStyles(e,A,i){let o=this._stateStyles.get("*");return e!==void 0&&(o=this._stateStyles.get(e?.toString())||o),o?o.buildStyles(A,i):new Map}build(e,A,i,o,n,g,r,s,a,Q){let c=[],f=this.ast.options&&this.ast.options.params||TD,m=r&&r.params||TD,p=this.buildStyles(i,m,c),M=s&&s.params||TD,K=this.buildStyles(o,M,c),W=new Set,DA=new Map,xA=new Map,wA=o==="void",wt={params:xv(M,f),delay:this.ast.options?.delay},we=Q?[]:Uv(e,A,this.ast.animation,n,g,p,K,wt,a,c),Fe=0;return we.forEach(he=>{Fe=Math.max(he.duration+he.delay,Fe)}),c.length?bv(A,this._triggerName,i,o,wA,p,K,[],[],DA,xA,Fe,c):(we.forEach(he=>{let ui=he.element,bo=Yt(DA,ui,new Set);he.preStyleProps.forEach(Ti=>bo.add(Ti));let Hi=Yt(xA,ui,new Set);he.postStyleProps.forEach(Ti=>Hi.add(Ti)),ui!==A&&W.add(ui)}),bv(A,this._triggerName,i,o,wA,p,K,we,[...W.values()],DA,xA,Fe))}};function gV(t,e,A,i,o){return t.some(n=>n(e,A,i,o))}function xv(t,e){let A=b({},e);return Object.entries(t).forEach(([i,o])=>{o!=null&&(A[i]=o)}),A}var XD=class{styles;defaultParams;normalizer;constructor(e,A,i){this.styles=e,this.defaultParams=A,this.normalizer=i}buildStyles(e,A){let i=new Map,o=xv(e,this.defaultParams);return this.styles.styles.forEach(n=>{typeof n!="string"&&n.forEach((g,r)=>{g&&(g=ys(g,o,A));let s=this.normalizer.normalizePropertyName(r,A);g=this.normalizer.normalizeStyleValue(r,s,g,A),i.set(r,g)})}),i}};function rV(t,e,A){return new $D(t,e,A)}var $D=class{name;ast;_normalizer;transitionFactories=[];fallbackTransition;states=new Map;constructor(e,A,i){this.name=e,this.ast=A,this._normalizer=i,A.states.forEach(o=>{let n=o.options&&o.options.params||{};this.states.set(o.name,new XD(o.style,n,i))}),Fv(this.states,"true","1"),Fv(this.states,"false","0"),A.transitions.forEach(o=>{this.transitionFactories.push(new Mc(e,o,this.states))}),this.fallbackTransition=sV(e,this.states)}get containsQueries(){return this.ast.queryCount>0}matchTransition(e,A,i,o){return this.transitionFactories.find(g=>g.match(e,A,i,o))||null}matchStyles(e,A,i){return this.fallbackTransition.buildStyles(e,A,i)}};function sV(t,e,A){let i=[(g,r)=>!0],o={type:UA.Sequence,steps:[],options:null},n={type:UA.Transition,animation:o,matchers:i,options:null,queryCount:0,depCount:0};return new Mc(t,n,e)}function Fv(t,e,A){t.has(e)?t.has(A)||t.set(A,t.get(e)):t.has(A)&&t.set(e,t.get(A))}var aV=new ZI,Af=class{bodyNode;_driver;_normalizer;_animations=new Map;_playersById=new Map;players=[];constructor(e,A,i){this.bodyNode=e,this._driver=A,this._normalizer=i}register(e,A){let i=[],o=[],n=Kv(this._driver,A,i,o);if(i.length)throw Cv(i);this._animations.set(e,n)}_buildPlayer(e,A,i){let o=e.element,n=GD(this._normalizer,e.keyframes,A,i);return this._driver.animate(o,n,e.duration,e.delay,e.easing,[],!0)}create(e,A,i={}){let o=[],n=this._animations.get(e),g,r=new Map;if(n?(g=Uv(this._driver,A,n,xD,Ec,new Map,new Map,i,aV,o),g.forEach(Q=>{let c=Yt(r,Q.element,new Map);Q.postStyleProps.forEach(f=>c.set(f,null))})):(o.push(Bv()),g=[]),o.length)throw Qv(o);r.forEach((Q,c)=>{Q.forEach((f,m)=>{Q.set(m,this._driver.computeStyle(c,m,ci))})});let s=g.map(Q=>{let c=r.get(Q.element);return this._buildPlayer(Q,new Map,c)}),a=nn(s);return this._playersById.set(e,a),a.onDestroy(()=>this.destroy(e)),this.players.push(a),a}destroy(e){let A=this._getPlayer(e);A.destroy(),this._playersById.delete(e);let i=this.players.indexOf(A);i>=0&&this.players.splice(i,1)}_getPlayer(e){let A=this._playersById.get(e);if(!A)throw Ev(e);return A}listen(e,A,i,o){let n=Bc(A,"","","");return Cc(this._getPlayer(e),i,n,o),()=>{}}command(e,A,i,o){if(i=="register"){this.register(e,o[0]);return}if(i=="create"){let g=o[0]||{};this.create(e,A,g);return}let n=this._getPlayer(e);switch(i){case"play":n.play();break;case"pause":n.pause();break;case"reset":n.reset();break;case"restart":n.restart();break;case"finish":n.finish();break;case"init":n.init();break;case"setPosition":n.setPosition(parseFloat(o[0]));break;case"destroy":this.destroy(e);break}}},vv="ng-animate-queued",IV=".ng-animate-queued",OD="ng-animate-disabled",CV=".ng-animate-disabled",BV="ng-star-inserted",QV=".ng-star-inserted",EV=[],Yv={namespaceId:"",setForRemoval:!1,setForMove:!1,hasAnimation:!1,removedBeforeQueried:!1},cV={namespaceId:"",setForMove:!1,setForRemoval:!1,hasAnimation:!1,removedBeforeQueried:!0},Ji="__ng_removed",qI=class{namespaceId;value;options;get params(){return this.options.params}constructor(e,A=""){this.namespaceId=A;let i=e&&e.hasOwnProperty("value"),o=i?e.value:e;if(this.value=dV(o),i){let n=e,{value:g}=n,r=Gc(n,["value"]);this.options=r}else this.options={};this.options.params||(this.options.params={})}absorbOptions(e){let A=e.params;if(A){let i=this.options.params;Object.keys(A).forEach(o=>{i[o]==null&&(i[o]=A[o])})}}},PI="void",PD=new qI(PI),ef=class{id;hostElement;_engine;players=[];_triggers=new Map;_queue=[];_elementListeners=new Map;_hostClassName;constructor(e,A,i){this.id=e,this.hostElement=A,this._engine=i,this._hostClassName="ng-tns-"+e,hi(A,this._hostClassName)}listen(e,A,i,o){if(!this._triggers.has(A))throw cv(i,A);if(i==null||i.length==0)throw lv(A);if(!hV(i))throw dv(i,A);let n=Yt(this._elementListeners,e,[]),g={name:A,phase:i,callback:o};n.push(g);let r=Yt(this._engine.statesByElement,e,new Map);return r.has(A)||(hi(e,HI),hi(e,HI+"-"+A),r.set(A,PD)),()=>{this._engine.afterFlush(()=>{let s=n.indexOf(g);s>=0&&n.splice(s,1),this._triggers.has(A)||r.delete(A)})}}register(e,A){return this._triggers.has(e)?!1:(this._triggers.set(e,A),!0)}_getTrigger(e){let A=this._triggers.get(e);if(!A)throw hv(e);return A}trigger(e,A,i,o=!0){let n=this._getTrigger(A),g=new VI(this.id,A,e),r=this._engine.statesByElement.get(e);r||(hi(e,HI),hi(e,HI+"-"+A),this._engine.statesByElement.set(e,r=new Map));let s=r.get(A),a=new qI(i,this.id);if(!(i&&i.hasOwnProperty("value"))&&s&&a.absorbOptions(s.options),r.set(A,a),s||(s=PD),!(a.value===PI)&&s.value===a.value){if(!DV(s.params,a.params)){let M=[],K=n.matchStyles(s.value,s.params,M),W=n.matchStyles(a.value,a.params,M);M.length?this._engine.reportError(M):this._engine.afterFlush(()=>{Tn(e,K),Yi(e,W)})}return}let f=Yt(this._engine.playersByElement,e,[]);f.forEach(M=>{M.namespaceId==this.id&&M.triggerName==A&&M.queued&&M.destroy()});let m=n.matchTransition(s.value,a.value,e,a.params),p=!1;if(!m){if(!o)return;m=n.fallbackTransition,p=!0}return this._engine.totalQueuedPlayers++,this._queue.push({element:e,triggerName:A,transition:m,fromState:s,toState:a,player:g,isFallbackTransition:p}),p||(hi(e,vv),g.onStart(()=>{Ms(e,vv)})),g.onDone(()=>{let M=this.players.indexOf(g);M>=0&&this.players.splice(M,1);let K=this._engine.playersByElement.get(e);if(K){let W=K.indexOf(g);W>=0&&K.splice(W,1)}}),this.players.push(g),f.push(g),g}deregister(e){this._triggers.delete(e),this._engine.statesByElement.forEach(A=>A.delete(e)),this._elementListeners.forEach((A,i)=>{this._elementListeners.set(i,A.filter(o=>o.name!=e))})}clearElementCache(e){this._engine.statesByElement.delete(e),this._elementListeners.delete(e);let A=this._engine.playersByElement.get(e);A&&(A.forEach(i=>i.destroy()),this._engine.playersByElement.delete(e))}_signalRemovalForInnerTriggers(e,A){let i=this._engine.driver.query(e,TI,!0);i.forEach(o=>{if(o[Ji])return;let n=this._engine.fetchNamespacesByElement(o);n.size?n.forEach(g=>g.triggerLeaveAnimation(o,A,!1,!0)):this.clearElementCache(o)}),this._engine.afterFlushAnimationsDone(()=>i.forEach(o=>this.clearElementCache(o)))}triggerLeaveAnimation(e,A,i,o){let n=this._engine.statesByElement.get(e),g=new Map;if(n){let r=[];if(n.forEach((s,a)=>{if(g.set(a,s.value),this._triggers.has(a)){let Q=this.trigger(e,a,PI,o);Q&&r.push(Q)}}),r.length)return this._engine.markElementAsRemoved(this.id,e,!0,A,g),i&&nn(r).onDone(()=>this._engine.processLeaveNode(e)),!0}return!1}prepareLeaveAnimationListeners(e){let A=this._elementListeners.get(e),i=this._engine.statesByElement.get(e);if(A&&i){let o=new Set;A.forEach(n=>{let g=n.name;if(o.has(g))return;o.add(g);let s=this._triggers.get(g).fallbackTransition,a=i.get(g)||PD,Q=new qI(PI),c=new VI(this.id,g,e);this._engine.totalQueuedPlayers++,this._queue.push({element:e,triggerName:g,transition:s,fromState:a,toState:Q,player:c,isFallbackTransition:!0})})}}removeNode(e,A){let i=this._engine;if(e.childElementCount&&this._signalRemovalForInnerTriggers(e,A),this.triggerLeaveAnimation(e,A,!0))return;let o=!1;if(i.totalAnimations){let n=i.players.length?i.playersByQueriedElement.get(e):[];if(n&&n.length)o=!0;else{let g=e;for(;g=g.parentNode;)if(i.statesByElement.get(g)){o=!0;break}}}if(this.prepareLeaveAnimationListeners(e),o)i.markElementAsRemoved(this.id,e,!1,A);else{let n=e[Ji];(!n||n===Yv)&&(i.afterFlush(()=>this.clearElementCache(e)),i.destroyInnerAnimations(e),i._onRemovalComplete(e,A))}}insertNode(e,A){hi(e,this._hostClassName)}drainQueuedTransitions(e){let A=[];return this._queue.forEach(i=>{let o=i.player;if(o.destroyed)return;let n=i.element,g=this._elementListeners.get(n);g&&g.forEach(r=>{if(r.name==i.triggerName){let s=Bc(n,i.triggerName,i.fromState.value,i.toState.value);s._data=e,Cc(i.player,r.phase,s,r.callback)}}),o.markedForDestroy?this._engine.afterFlush(()=>{o.destroy()}):A.push(i)}),this._queue=[],A.sort((i,o)=>{let n=i.transition.ast.depCount,g=o.transition.ast.depCount;return n==0||g==0?n-g:this._engine.driver.containsElement(i.element,o.element)?1:-1})}destroy(e){this.players.forEach(A=>A.destroy()),this._signalRemovalForInnerTriggers(this.hostElement,e)}},tf=class{bodyNode;driver;_normalizer;players=[];newHostElements=new Map;playersByElement=new Map;playersByQueriedElement=new Map;statesByElement=new Map;disabledNodes=new Set;totalAnimations=0;totalQueuedPlayers=0;_namespaceLookup={};_namespaceList=[];_flushFns=[];_whenQuietFns=[];namespacesByHostElement=new Map;collectedEnterElements=[];collectedLeaveElements=[];onRemovalComplete=(e,A)=>{};_onRemovalComplete(e,A){this.onRemovalComplete(e,A)}constructor(e,A,i){this.bodyNode=e,this.driver=A,this._normalizer=i}get queuedPlayers(){let e=[];return this._namespaceList.forEach(A=>{A.players.forEach(i=>{i.queued&&e.push(i)})}),e}createNamespace(e,A){let i=new ef(e,A,this);return this.bodyNode&&this.driver.containsElement(this.bodyNode,A)?this._balanceNamespaceList(i,A):(this.newHostElements.set(A,i),this.collectEnterElement(A)),this._namespaceLookup[e]=i}_balanceNamespaceList(e,A){let i=this._namespaceList,o=this.namespacesByHostElement;if(i.length-1>=0){let g=!1,r=this.driver.getParentElement(A);for(;r;){let s=o.get(r);if(s){let a=i.indexOf(s);i.splice(a+1,0,e),g=!0;break}r=this.driver.getParentElement(r)}g||i.unshift(e)}else i.push(e);return o.set(A,e),e}register(e,A){let i=this._namespaceLookup[e];return i||(i=this.createNamespace(e,A)),i}registerTrigger(e,A,i){let o=this._namespaceLookup[e];o&&o.register(A,i)&&this.totalAnimations++}destroy(e,A){e&&(this.afterFlush(()=>{}),this.afterFlushAnimationsDone(()=>{let i=this._fetchNamespace(e);this.namespacesByHostElement.delete(i.hostElement);let o=this._namespaceList.indexOf(i);o>=0&&this._namespaceList.splice(o,1),i.destroy(A),delete this._namespaceLookup[e]}))}_fetchNamespace(e){return this._namespaceLookup[e]}fetchNamespacesByElement(e){let A=new Set,i=this.statesByElement.get(e);if(i){for(let o of i.values())if(o.namespaceId){let n=this._fetchNamespace(o.namespaceId);n&&A.add(n)}}return A}trigger(e,A,i,o){if(mc(A)){let n=this._fetchNamespace(e);if(n)return n.trigger(A,i,o),!0}return!1}insertNode(e,A,i,o){if(!mc(A))return;let n=A[Ji];if(n&&n.setForRemoval){n.setForRemoval=!1,n.setForMove=!0;let g=this.collectedLeaveElements.indexOf(A);g>=0&&this.collectedLeaveElements.splice(g,1)}if(e){let g=this._fetchNamespace(e);g&&g.insertNode(A,i)}o&&this.collectEnterElement(A)}collectEnterElement(e){this.collectedEnterElements.push(e)}markElementAsDisabled(e,A){A?this.disabledNodes.has(e)||(this.disabledNodes.add(e),hi(e,OD)):this.disabledNodes.has(e)&&(this.disabledNodes.delete(e),Ms(e,OD))}removeNode(e,A,i){if(mc(A)){let o=e?this._fetchNamespace(e):null;o?o.removeNode(A,i):this.markElementAsRemoved(e,A,!1,i);let n=this.namespacesByHostElement.get(A);n&&n.id!==e&&n.removeNode(A,i)}else this._onRemovalComplete(A,i)}markElementAsRemoved(e,A,i,o,n){this.collectedLeaveElements.push(A),A[Ji]={namespaceId:e,setForRemoval:o,hasAnimation:i,removedBeforeQueried:!1,previousTriggersValues:n}}listen(e,A,i,o,n){return mc(A)?this._fetchNamespace(e).listen(A,i,o,n):()=>{}}_buildInstruction(e,A,i,o,n){return e.transition.build(this.driver,e.element,e.fromState.value,e.toState.value,i,o,e.fromState.options,e.toState.options,A,n)}destroyInnerAnimations(e){let A=this.driver.query(e,TI,!0);A.forEach(i=>this.destroyActiveAnimationsForElement(i)),this.playersByQueriedElement.size!=0&&(A=this.driver.query(e,cc,!0),A.forEach(i=>this.finishActiveQueriedAnimationOnElement(i)))}destroyActiveAnimationsForElement(e){let A=this.playersByElement.get(e);A&&A.forEach(i=>{i.queued?i.markedForDestroy=!0:i.destroy()})}finishActiveQueriedAnimationOnElement(e){let A=this.playersByQueriedElement.get(e);A&&A.forEach(i=>i.finish())}whenRenderingDone(){return new Promise(e=>{if(this.players.length)return nn(this.players).onDone(()=>e());e()})}processLeaveNode(e){let A=e[Ji];if(A&&A.setForRemoval){if(e[Ji]=Yv,A.namespaceId){this.destroyInnerAnimations(e);let i=this._fetchNamespace(A.namespaceId);i&&i.clearElementCache(e)}this._onRemovalComplete(e,A.setForRemoval)}e.classList?.contains(OD)&&this.markElementAsDisabled(e,!1),this.driver.query(e,CV,!0).forEach(i=>{this.markElementAsDisabled(i,!1)})}flush(e=-1){let A=[];if(this.newHostElements.size&&(this.newHostElements.forEach((i,o)=>this._balanceNamespaceList(i,o)),this.newHostElements.clear()),this.totalAnimations&&this.collectedEnterElements.length)for(let i=0;i<this.collectedEnterElements.length;i++){let o=this.collectedEnterElements[i];hi(o,BV)}if(this._namespaceList.length&&(this.totalQueuedPlayers||this.collectedLeaveElements.length)){let i=[];try{A=this._flushAnimations(i,e)}finally{for(let o=0;o<i.length;o++)i[o]()}}else for(let i=0;i<this.collectedLeaveElements.length;i++){let o=this.collectedLeaveElements[i];this.processLeaveNode(o)}if(this.totalQueuedPlayers=0,this.collectedEnterElements.length=0,this.collectedLeaveElements.length=0,this._flushFns.forEach(i=>i()),this._flushFns=[],this._whenQuietFns.length){let i=this._whenQuietFns;this._whenQuietFns=[],A.length?nn(A).onDone(()=>{i.forEach(o=>o())}):i.forEach(o=>o())}}reportError(e){throw uv(e)}_flushAnimations(e,A){let i=new ZI,o=[],n=new Map,g=[],r=new Map,s=new Map,a=new Map,Q=new Set;this.disabledNodes.forEach(E=>{Q.add(E);let oA=this.driver.query(E,IV,!0);for(let fA=0;fA<oA.length;fA++)Q.add(oA[fA])});let c=this.bodyNode,f=Array.from(this.statesByElement.keys()),m=Gv(f,this.collectedEnterElements),p=new Map,M=0;m.forEach((E,oA)=>{let fA=xD+M++;p.set(oA,fA),E.forEach(VA=>hi(VA,fA))});let K=[],W=new Set,DA=new Set;for(let E=0;E<this.collectedLeaveElements.length;E++){let oA=this.collectedLeaveElements[E],fA=oA[Ji];fA&&fA.setForRemoval&&(K.push(oA),W.add(oA),fA.hasAnimation?this.driver.query(oA,QV,!0).forEach(VA=>W.add(VA)):DA.add(oA))}let xA=new Map,wA=Gv(f,Array.from(W));wA.forEach((E,oA)=>{let fA=Ec+M++;xA.set(oA,fA),E.forEach(VA=>hi(VA,fA))}),e.push(()=>{m.forEach((E,oA)=>{let fA=p.get(oA);E.forEach(VA=>Ms(VA,fA))}),wA.forEach((E,oA)=>{let fA=xA.get(oA);E.forEach(VA=>Ms(VA,fA))}),K.forEach(E=>{this.processLeaveNode(E)})});let wt=[],we=[];for(let E=this._namespaceList.length-1;E>=0;E--)this._namespaceList[E].drainQueuedTransitions(A).forEach(fA=>{let VA=fA.player,Ne=fA.element;if(wt.push(VA),this.collectedEnterElements.length){let He=Ne[Ji];if(He&&He.setForMove){if(He.previousTriggersValues&&He.previousTriggersValues.has(fA.triggerName)){let Oi=He.previousTriggersValues.get(fA.triggerName),ht=this.statesByElement.get(fA.element);if(ht&&ht.has(fA.triggerName)){let On=ht.get(fA.triggerName);On.value=Oi,ht.set(fA.triggerName,On)}}VA.destroy();return}}let tt=!c||!this.driver.containsElement(c,Ne),dt=xA.get(Ne),ni=p.get(Ne),oe=this._buildInstruction(fA,i,ni,dt,tt);if(oe.errors&&oe.errors.length){we.push(oe);return}if(tt){VA.onStart(()=>Tn(Ne,oe.fromStyles)),VA.onDestroy(()=>Yi(Ne,oe.toStyles)),o.push(VA);return}if(fA.isFallbackTransition){VA.onStart(()=>Tn(Ne,oe.fromStyles)),VA.onDestroy(()=>Yi(Ne,oe.toStyles)),o.push(VA);return}let zI=[];oe.timelines.forEach(He=>{He.stretchStartingKeyframe=!0,this.disabledNodes.has(He.element)||zI.push(He)}),oe.timelines=zI,i.append(Ne,oe.timelines);let jI={instruction:oe,player:VA,element:Ne};g.push(jI),oe.queriedElements.forEach(He=>Yt(r,He,[]).push(VA)),oe.preStyleProps.forEach((He,Oi)=>{if(He.size){let ht=s.get(Oi);ht||s.set(Oi,ht=new Set),He.forEach((On,ks)=>ht.add(ks))}}),oe.postStyleProps.forEach((He,Oi)=>{let ht=a.get(Oi);ht||a.set(Oi,ht=new Set),He.forEach((On,ks)=>ht.add(ks))})});if(we.length){let E=[];we.forEach(oA=>{E.push(mv(oA.triggerName,oA.errors))}),wt.forEach(oA=>oA.destroy()),this.reportError(E)}let Fe=new Map,he=new Map;g.forEach(E=>{let oA=E.element;i.has(oA)&&(he.set(oA,oA),this._beforeAnimationBuild(E.player.namespaceId,E.instruction,Fe))}),o.forEach(E=>{let oA=E.element;this._getPreviousPlayers(oA,!1,E.namespaceId,E.triggerName,null).forEach(VA=>{Yt(Fe,oA,[]).push(VA),VA.destroy()})});let ui=K.filter(E=>Lv(E,s,a)),bo=new Map;Nv(bo,this.driver,DA,a,ci).forEach(E=>{Lv(E,s,a)&&ui.push(E)});let Ti=new Map;m.forEach((E,oA)=>{Nv(Ti,this.driver,new Set(E),s,Is)}),ui.forEach(E=>{let oA=bo.get(E),fA=Ti.get(E);bo.set(E,new Map([...oA?.entries()??[],...fA?.entries()??[]]))});let Zg=[],JA=[],qg={};g.forEach(E=>{let{element:oA,player:fA,instruction:VA}=E;if(i.has(oA)){if(Q.has(oA)){fA.onDestroy(()=>Yi(oA,VA.toStyles)),fA.disabled=!0,fA.overrideTotalTime(VA.totalTime),o.push(fA);return}let Ne=qg;if(he.size>1){let dt=oA,ni=[];for(;dt=dt.parentNode;){let oe=he.get(dt);if(oe){Ne=oe;break}ni.push(dt)}ni.forEach(oe=>he.set(oe,Ne))}let tt=this._buildAnimation(fA.namespaceId,VA,Fe,n,Ti,bo);if(fA.setRealPlayer(tt),Ne===qg)Zg.push(fA);else{let dt=this.playersByElement.get(Ne);dt&&dt.length&&(fA.parentPlayer=nn(dt)),o.push(fA)}}else Tn(oA,VA.fromStyles),fA.onDestroy(()=>Yi(oA,VA.toStyles)),JA.push(fA),Q.has(oA)&&o.push(fA)}),JA.forEach(E=>{let oA=n.get(E.element);if(oA&&oA.length){let fA=nn(oA);E.setRealPlayer(fA)}}),o.forEach(E=>{E.parentPlayer?E.syncPlayerEvents(E.parentPlayer):E.destroy()});for(let E=0;E<K.length;E++){let oA=K[E],fA=oA[Ji];if(Ms(oA,Ec),fA&&fA.hasAnimation)continue;let VA=[];if(r.size){let tt=r.get(oA);tt&&tt.length&&VA.push(...tt);let dt=this.driver.query(oA,cc,!0);for(let ni=0;ni<dt.length;ni++){let oe=r.get(dt[ni]);oe&&oe.length&&VA.push(...oe)}}let Ne=VA.filter(tt=>!tt.destroyed);Ne.length?uV(this,oA,Ne):this.processLeaveNode(oA)}return K.length=0,Zg.forEach(E=>{this.players.push(E),E.onDone(()=>{E.destroy();let oA=this.players.indexOf(E);this.players.splice(oA,1)}),E.play()}),Zg}afterFlush(e){this._flushFns.push(e)}afterFlushAnimationsDone(e){this._whenQuietFns.push(e)}_getPreviousPlayers(e,A,i,o,n){let g=[];if(A){let r=this.playersByQueriedElement.get(e);r&&(g=r)}else{let r=this.playersByElement.get(e);if(r){let s=!n||n==PI;r.forEach(a=>{a.queued||!s&&a.triggerName!=o||g.push(a)})}}return(i||o)&&(g=g.filter(r=>!(i&&i!=r.namespaceId||o&&o!=r.triggerName))),g}_beforeAnimationBuild(e,A,i){let o=A.triggerName,n=A.element,g=A.isRemovalTransition?void 0:e,r=A.isRemovalTransition?void 0:o;for(let s of A.timelines){let a=s.element,Q=a!==n,c=Yt(i,a,[]);this._getPreviousPlayers(a,Q,g,r,A.toState).forEach(m=>{let p=m.getRealPlayer();p.beforeDestroy&&p.beforeDestroy(),m.destroy(),c.push(m)})}Tn(n,A.fromStyles)}_buildAnimation(e,A,i,o,n,g){let r=A.triggerName,s=A.element,a=[],Q=new Set,c=new Set,f=A.timelines.map(p=>{let M=p.element;Q.add(M);let K=M[Ji];if(K&&K.removedBeforeQueried)return new co(p.duration,p.delay);let W=M!==s,DA=mV((i.get(M)||EV).map(Fe=>Fe.getRealPlayer())).filter(Fe=>{let he=Fe;return he.element?he.element===M:!1}),xA=n.get(M),wA=g.get(M),wt=GD(this._normalizer,p.keyframes,xA,wA),we=this._buildPlayer(p,wt,DA);if(p.subTimeline&&o&&c.add(M),W){let Fe=new VI(e,r,M);Fe.setRealPlayer(we),a.push(Fe)}return we});a.forEach(p=>{Yt(this.playersByQueriedElement,p.element,[]).push(p),p.onDone(()=>lV(this.playersByQueriedElement,p.element,p))}),Q.forEach(p=>hi(p,YD));let m=nn(f);return m.onDestroy(()=>{Q.forEach(p=>Ms(p,YD)),Yi(s,A.toStyles)}),c.forEach(p=>{Yt(o,p,[]).push(m)}),m}_buildPlayer(e,A,i){return A.length>0?this.driver.animate(e.element,A,e.duration,e.delay,e.easing,i):new co(e.duration,e.delay)}},VI=class{namespaceId;triggerName;element;_player=new co;_containsRealPlayer=!1;_queuedCallbacks=new Map;destroyed=!1;parentPlayer=null;markedForDestroy=!1;disabled=!1;queued=!0;totalTime=0;constructor(e,A,i){this.namespaceId=e,this.triggerName=A,this.element=i}setRealPlayer(e){this._containsRealPlayer||(this._player=e,this._queuedCallbacks.forEach((A,i)=>{A.forEach(o=>Cc(e,i,void 0,o))}),this._queuedCallbacks.clear(),this._containsRealPlayer=!0,this.overrideTotalTime(e.totalTime),this.queued=!1)}getRealPlayer(){return this._player}overrideTotalTime(e){this.totalTime=e}syncPlayerEvents(e){let A=this._player;A.triggerCallback&&e.onStart(()=>A.triggerCallback("start")),e.onDone(()=>this.finish()),e.onDestroy(()=>this.destroy())}_queueEvent(e,A){Yt(this._queuedCallbacks,e,[]).push(A)}onDone(e){this.queued&&this._queueEvent("done",e),this._player.onDone(e)}onStart(e){this.queued&&this._queueEvent("start",e),this._player.onStart(e)}onDestroy(e){this.queued&&this._queueEvent("destroy",e),this._player.onDestroy(e)}init(){this._player.init()}hasStarted(){return this.queued?!1:this._player.hasStarted()}play(){!this.queued&&this._player.play()}pause(){!this.queued&&this._player.pause()}restart(){!this.queued&&this._player.restart()}finish(){this._player.finish()}destroy(){this.destroyed=!0,this._player.destroy()}reset(){!this.queued&&this._player.reset()}setPosition(e){this.queued||this._player.setPosition(e)}getPosition(){return this.queued?0:this._player.getPosition()}triggerCallback(e){let A=this._player;A.triggerCallback&&A.triggerCallback(e)}};function lV(t,e,A){let i=t.get(e);if(i){if(i.length){let o=i.indexOf(A);i.splice(o,1)}i.length==0&&t.delete(e)}return i}function dV(t){return t??null}function mc(t){return t&&t.nodeType===1}function hV(t){return t=="start"||t=="done"}function Sv(t,e){let A=t.style.display;return t.style.display=e??"none",A}function Nv(t,e,A,i,o){let n=[];A.forEach(s=>n.push(Sv(s)));let g=[];i.forEach((s,a)=>{let Q=new Map;s.forEach(c=>{let f=e.computeStyle(a,c,o);Q.set(c,f),(!f||f.length==0)&&(a[Ji]=cV,g.push(a))}),t.set(a,Q)});let r=0;return A.forEach(s=>Sv(s,n[r++])),g}function Gv(t,e){let A=new Map;if(t.forEach(r=>A.set(r,[])),e.length==0)return A;let i=1,o=new Set(e),n=new Map;function g(r){if(!r)return i;let s=n.get(r);if(s)return s;let a=r.parentNode;return A.has(a)?s=a:o.has(a)?s=i:s=g(a),n.set(r,s),s}return e.forEach(r=>{let s=g(r);s!==i&&A.get(s).push(r)}),A}function hi(t,e){t.classList?.add(e)}function Ms(t,e){t.classList?.remove(e)}function uV(t,e,A){nn(A).onDone(()=>t.processLeaveNode(e))}function mV(t){let e=[];return Jv(t,e),e}function Jv(t,e){for(let A=0;A<t.length;A++){let i=t[A];i instanceof Sg?Jv(i.players,e):e.push(i)}}function DV(t,e){let A=Object.keys(t),i=Object.keys(e);if(A.length!=i.length)return!1;for(let o=0;o<A.length;o++){let n=A[o];if(!e.hasOwnProperty(n)||t[n]!==e[n])return!1}return!0}function Lv(t,e,A){let i=A.get(t);if(!i)return!1;let o=e.get(t);return o?i.forEach(n=>o.add(n)):e.set(t,i),A.delete(t),!0}var Rs=class{_driver;_normalizer;_transitionEngine;_timelineEngine;_triggerCache={};onRemovalComplete=(e,A)=>{};constructor(e,A,i){this._driver=A,this._normalizer=i,this._transitionEngine=new tf(e.body,A,i),this._timelineEngine=new Af(e.body,A,i),this._transitionEngine.onRemovalComplete=(o,n)=>this.onRemovalComplete(o,n)}registerTrigger(e,A,i,o,n){let g=e+"-"+o,r=this._triggerCache[g];if(!r){let s=[],a=[],Q=Kv(this._driver,n,s,a);if(s.length)throw Iv(o,s);r=rV(o,Q,this._normalizer),this._triggerCache[g]=r}this._transitionEngine.registerTrigger(A,o,r)}register(e,A){this._transitionEngine.register(e,A)}destroy(e,A){this._transitionEngine.destroy(e,A)}onInsert(e,A,i,o){this._transitionEngine.insertNode(e,A,i,o)}onRemove(e,A,i){this._transitionEngine.removeNode(e,A,i)}disableAnimations(e,A){this._transitionEngine.markElementAsDisabled(e,A)}process(e,A,i,o){if(i.charAt(0)=="@"){let[n,g]=LD(i),r=o;this._timelineEngine.command(n,A,g,r)}else this._transitionEngine.trigger(e,A,i,o)}listen(e,A,i,o,n){if(i.charAt(0)=="@"){let[g,r]=LD(i);return this._timelineEngine.listen(g,A,r,n)}return this._transitionEngine.listen(e,A,i,o,n)}flush(e=-1){this._transitionEngine.flush(e)}get players(){return[...this._transitionEngine.players,...this._timelineEngine.players]}whenRenderingDone(){return this._transitionEngine.whenRenderingDone()}afterFlushAnimationsDone(e){this._transitionEngine.afterFlushAnimationsDone(e)}};function fV(t,e){let A=null,i=null;return Array.isArray(e)&&e.length?(A=ZD(e[0]),e.length>1&&(i=ZD(e[e.length-1]))):e instanceof Map&&(A=ZD(e)),A||i?new pV(t,A,i):null}var pV=(()=>{class t{_element;_startStyles;_endStyles;static initialStylesByElement=new WeakMap;_state=0;_initialStyles;constructor(A,i,o){this._element=A,this._startStyles=i,this._endStyles=o;let n=t.initialStylesByElement.get(A);n||t.initialStylesByElement.set(A,n=new Map),this._initialStyles=n}start(){this._state<1&&(this._startStyles&&Yi(this._element,this._startStyles,this._initialStyles),this._state=1)}finish(){this.start(),this._state<2&&(Yi(this._element,this._initialStyles),this._endStyles&&(Yi(this._element,this._endStyles),this._endStyles=null),this._state=1)}destroy(){this.finish(),this._state<3&&(t.initialStylesByElement.delete(this._element),this._startStyles&&(Tn(this._element,this._startStyles),this._endStyles=null),this._endStyles&&(Tn(this._element,this._endStyles),this._endStyles=null),Yi(this._element,this._initialStyles),this._state=3)}}return t})();function ZD(t){let e=null;return t.forEach((A,i)=>{wV(i)&&(e=e||new Map,e.set(i,A))}),e}function wV(t){return t==="display"||t==="position"}var Rc=class{element;keyframes;options;_specialStyles;_onDoneFns=[];_onStartFns=[];_onDestroyFns=[];_duration;_delay;_initialized=!1;_finished=!1;_started=!1;_destroyed=!1;_finalKeyframe;_originalOnDoneFns=[];_originalOnStartFns=[];domPlayer;time=0;parentPlayer=null;currentSnapshot=new Map;constructor(e,A,i,o){this.element=e,this.keyframes=A,this.options=i,this._specialStyles=o,this._duration=i.duration,this._delay=i.delay||0,this.time=this._duration+this._delay}_onFinish(){this._finished||(this._finished=!0,this._onDoneFns.forEach(e=>e()),this._onDoneFns=[])}init(){this._buildPlayer(),this._preparePlayerBeforeStart()}_buildPlayer(){if(this._initialized)return;this._initialized=!0;let e=this.keyframes;this.domPlayer=this._triggerWebAnimation(this.element,e,this.options),this._finalKeyframe=e.length?e[e.length-1]:new Map;let A=()=>this._onFinish();this.domPlayer.addEventListener("finish",A),this.onDestroy(()=>{this.domPlayer.removeEventListener("finish",A)})}_preparePlayerBeforeStart(){this._delay?this._resetDomPlayerState():this.domPlayer.pause()}_convertKeyframesToObject(e){let A=[];return e.forEach(i=>{A.push(Object.fromEntries(i))}),A}_triggerWebAnimation(e,A,i){return e.animate(this._convertKeyframesToObject(A),i)}onStart(e){this._originalOnStartFns.push(e),this._onStartFns.push(e)}onDone(e){this._originalOnDoneFns.push(e),this._onDoneFns.push(e)}onDestroy(e){this._onDestroyFns.push(e)}play(){this._buildPlayer(),this.hasStarted()||(this._onStartFns.forEach(e=>e()),this._onStartFns=[],this._started=!0,this._specialStyles&&this._specialStyles.start()),this.domPlayer.play()}pause(){this.init(),this.domPlayer.pause()}finish(){this.init(),this._specialStyles&&this._specialStyles.finish(),this._onFinish(),this.domPlayer.finish()}reset(){this._resetDomPlayerState(),this._destroyed=!1,this._finished=!1,this._started=!1,this._onStartFns=this._originalOnStartFns,this._onDoneFns=this._originalOnDoneFns}_resetDomPlayerState(){this.domPlayer&&this.domPlayer.cancel()}restart(){this.reset(),this.play()}hasStarted(){return this._started}destroy(){this._destroyed||(this._destroyed=!0,this._resetDomPlayerState(),this._onFinish(),this._specialStyles&&this._specialStyles.destroy(),this._onDestroyFns.forEach(e=>e()),this._onDestroyFns=[])}setPosition(e){this.domPlayer===void 0&&this.init(),this.domPlayer.currentTime=e*this.time}getPosition(){return+(this.domPlayer.currentTime??0)/this.time}get totalTime(){return this._delay+this._duration}beforeDestroy(){let e=new Map;this.hasStarted()&&this._finalKeyframe.forEach((i,o)=>{o!=="offset"&&e.set(o,this._finished?i:dc(this.element,o))}),this.currentSnapshot=e}triggerCallback(e){let A=e==="start"?this._onStartFns:this._onDoneFns;A.forEach(i=>i()),A.length=0}},kc=class{validateStyleProperty(e){return!0}validateAnimatableStyleProperty(e){return!0}containsElement(e,A){return _D(e,A)}getParentElement(e){return Qc(e)}query(e,A,i){return KD(e,A,i)}computeStyle(e,A,i){return dc(e,A)}animate(e,A,i,o,n,g=[]){let r=o==0?"both":"forwards",s={duration:i,delay:o,fill:r};n&&(s.easing=n);let a=new Map,Q=g.filter(m=>m instanceof Rc);wv(i,o)&&Q.forEach(m=>{m.currentSnapshot.forEach((p,M)=>a.set(M,p))});let c=fv(A).map(m=>new Map(m));c=yv(e,c,a);let f=fV(e,c);return new Rc(e,c,s,f)}};var Dc="@",Hv="@.disabled",bc=class{namespaceId;delegate;engine;_onDestroy;\u0275type=0;constructor(e,A,i,o){this.namespaceId=e,this.delegate=A,this.engine=i,this._onDestroy=o}get data(){return this.delegate.data}destroyNode(e){this.delegate.destroyNode?.(e)}destroy(){this.engine.destroy(this.namespaceId,this.delegate),this.engine.afterFlushAnimationsDone(()=>{queueMicrotask(()=>{this.delegate.destroy()})}),this._onDestroy?.()}createElement(e,A){return this.delegate.createElement(e,A)}createComment(e){return this.delegate.createComment(e)}createText(e){return this.delegate.createText(e)}appendChild(e,A){this.delegate.appendChild(e,A),this.engine.onInsert(this.namespaceId,A,e,!1)}insertBefore(e,A,i,o=!0){this.delegate.insertBefore(e,A,i),this.engine.onInsert(this.namespaceId,A,e,o)}removeChild(e,A,i){this.parentNode(A)&&this.engine.onRemove(this.namespaceId,A,this.delegate)}selectRootElement(e,A){return this.delegate.selectRootElement(e,A)}parentNode(e){return this.delegate.parentNode(e)}nextSibling(e){return this.delegate.nextSibling(e)}setAttribute(e,A,i,o){this.delegate.setAttribute(e,A,i,o)}removeAttribute(e,A,i){this.delegate.removeAttribute(e,A,i)}addClass(e,A){this.delegate.addClass(e,A)}removeClass(e,A){this.delegate.removeClass(e,A)}setStyle(e,A,i,o){this.delegate.setStyle(e,A,i,o)}removeStyle(e,A,i){this.delegate.removeStyle(e,A,i)}setProperty(e,A,i){A.charAt(0)==Dc&&A==Hv?this.disableAnimations(e,!!i):this.delegate.setProperty(e,A,i)}setValue(e,A){this.delegate.setValue(e,A)}listen(e,A,i,o){return this.delegate.listen(e,A,i,o)}disableAnimations(e,A){this.engine.disableAnimations(e,A)}},of=class extends bc{factory;constructor(e,A,i,o,n){super(A,i,o,n),this.factory=e,this.namespaceId=A}setProperty(e,A,i){A.charAt(0)==Dc?A.charAt(1)=="."&&A==Hv?(i=i===void 0?!0:!!i,this.disableAnimations(e,i)):this.engine.process(this.namespaceId,e,A.slice(1),i):this.delegate.setProperty(e,A,i)}listen(e,A,i,o){if(A.charAt(0)==Dc){let n=yV(e),g=A.slice(1),r="";return g.charAt(0)!=Dc&&([g,r]=MV(g)),this.engine.listen(this.namespaceId,n,g,r,s=>{let a=s._data||-1;this.factory.scheduleListenerCallback(a,i,s)})}return this.delegate.listen(e,A,i,o)}};function yV(t){switch(t){case"body":return document.body;case"document":return document;case"window":return window;default:return t}}function MV(t){let e=t.indexOf("."),A=t.substring(0,e),i=t.slice(e+1);return[A,i]}var Fc=class{delegate;engine;_zone;_currentId=0;_microtaskId=1;_animationCallbacksBuffer=[];_rendererCache=new Map;_cdRecurDepth=0;constructor(e,A,i){this.delegate=e,this.engine=A,this._zone=i,A.onRemovalComplete=(o,n)=>{n?.removeChild(null,o)}}createRenderer(e,A){let i="",o=this.delegate.createRenderer(e,A);if(!e||!A?.data?.animation){let a=this._rendererCache,Q=a.get(o);if(!Q){let c=()=>a.delete(o);Q=new bc(i,o,this.engine,c),a.set(o,Q)}return Q}let n=A.id,g=A.id+"-"+this._currentId;this._currentId++,this.engine.register(g,e);let r=a=>{Array.isArray(a)?a.forEach(r):this.engine.registerTrigger(n,g,e,a.name,a)};return A.data.animation.forEach(r),new of(this,g,o,this.engine)}begin(){this._cdRecurDepth++,this.delegate.begin&&this.delegate.begin()}_scheduleCountTask(){queueMicrotask(()=>{this._microtaskId++})}scheduleListenerCallback(e,A,i){if(e>=0&&e<this._microtaskId){this._zone.run(()=>A(i));return}let o=this._animationCallbacksBuffer;o.length==0&&queueMicrotask(()=>{this._zone.run(()=>{o.forEach(n=>{let[g,r]=n;g(r)}),this._animationCallbacksBuffer=[]})}),o.push([A,i])}end(){this._cdRecurDepth--,this._cdRecurDepth==0&&this._zone.runOutsideAngular(()=>{this._scheduleCountTask(),this.engine.flush(this._microtaskId)}),this.delegate.end&&this.delegate.end()}whenRenderingDone(){return this.engine.whenRenderingDone()}componentReplaced(e){this.engine.flush(),this.delegate.componentReplaced?.(e)}};var kV=(()=>{class t extends Rs{constructor(A,i,o){super(A,i,o)}ngOnDestroy(){this.flush()}static \u0275fac=function(i){return new(i||t)(Z(cA),Z(Og),Z(Pg))};static \u0275prov=S({token:t,factory:t.\u0275fac})}return t})();function bV(){return new fc}function FV(t,e,A){return new Fc(t,e,A)}var Ov=[{provide:Pg,useFactory:bV},{provide:Rs,useClass:kV},{provide:Bt,useFactory:FV,deps:[ka,Rs,tA]}],vV=[{provide:Og,useClass:nf},{provide:Ae,useValue:"NoopAnimations"},...Ov],Tv=[{provide:Og,useFactory:()=>new kc},{provide:Ae,useFactory:()=>"BrowserAnimations"},...Ov],Pv=(()=>{class t{static withConfig(A){return{ngModule:t,providers:A.disableAnimations?vV:Tv}}static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({providers:Tv,imports:[Fa]})}return t})();var SV=new F("mat-chips-default-options",{providedIn:"root",factory:()=>({separatorKeyCodes:[13]})});var Zv=(()=>{class t{static \u0275fac=function(i){return new(i||t)};static \u0275mod=X({type:t});static \u0275inj=j({providers:[ns,{provide:SV,useValue:{separatorKeyCodes:[13]}}],imports:[mA,jo,mA]})}return t})();var vc=class t{static \u0275fac=function(A){return new(A||t)};static \u0275mod=X({type:t});static \u0275inj=j({imports:[Zo,kQ,rF,ub,tn,$E,Xo,zk,Xo,tF,sF,BF,mF,KE,pb,Jb,UE,pF,zb,OF.forRoot(),PF,ZM,Zv,nF]})};var WI=class t{static \u0275fac=function(A){return new(A||t)};static \u0275mod=X({type:t,bootstrap:[ps]});static \u0275inj=j({providers:[wo,Un,yo,hs,us,ms,po,ds,Jn],imports:[vc,Fa,kQ,ru,Ic,$E,tn,Xo,Pv,Xo]})};fetch("./assets/config/runtime-config.json").then(t=>t.json()).then(t=>{window.runtimeConfig=t,rQ().bootstrapModule(WI).catch(e=>console.error(e))});rQ().bootstrapModule(WI).catch(t=>console.error(t));
================================================
File: src/google/adk/cli/browser/polyfills-B6TNHZQ6.js
================================================
/**
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
================================================
File: src/google/adk/cli/browser/styles-4VDSPQ37.css
================================================
/**
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
html{color-scheme:dark}html{--mat-sys-background: light-dark(#fcf9f8, #131314);--mat-sys-error: light-dark(#ba1a1a, #ffb4ab);--mat-sys-error-container: light-dark(#ffdad6, #93000a);--mat-sys-inverse-on-surface: light-dark(#f3f0f0, #313030);--mat-sys-inverse-primary: light-dark(#c1c7cd, #595f65);--mat-sys-inverse-surface: light-dark(#313030, #e5e2e2);--mat-sys-on-background: light-dark(#1c1b1c, #e5e2e2);--mat-sys-on-error: light-dark(#ffffff, #690005);--mat-sys-on-error-container: light-dark(#410002, #ffdad6);--mat-sys-on-primary: light-dark(#ffffff, #2b3136);--mat-sys-on-primary-container: light-dark(#161c21, #dde3e9);--mat-sys-on-primary-fixed: light-dark(#161c21, #161c21);--mat-sys-on-primary-fixed-variant: light-dark(#41474d, #41474d);--mat-sys-on-secondary: light-dark(#ffffff, #003061);--mat-sys-on-secondary-container: light-dark(#001b3c, #d5e3ff);--mat-sys-on-secondary-fixed: light-dark(#001b3c, #001b3c);--mat-sys-on-secondary-fixed-variant: light-dark(#0f4784, #0f4784);--mat-sys-on-surface: light-dark(#1c1b1c, #e5e2e2);--mat-sys-on-surface-variant: light-dark(#44474a, #e1e2e6);--mat-sys-on-tertiary: light-dark(#ffffff, #2b3136);--mat-sys-on-tertiary-container: light-dark(#161c21, #dde3e9);--mat-sys-on-tertiary-fixed: light-dark(#161c21, #161c21);--mat-sys-on-tertiary-fixed-variant: light-dark(#41474d, #41474d);--mat-sys-outline: light-dark(#74777b, #8e9194);--mat-sys-outline-variant: light-dark(#c4c7ca, #44474a);--mat-sys-primary: light-dark(#595f65, #c1c7cd);--mat-sys-primary-container: light-dark(#dde3e9, #41474d);--mat-sys-primary-fixed: light-dark(#dde3e9, #dde3e9);--mat-sys-primary-fixed-dim: light-dark(#c1c7cd, #c1c7cd);--mat-sys-scrim: light-dark(#000000, #000000);--mat-sys-secondary: light-dark(#305f9d, #a7c8ff);--mat-sys-secondary-container: light-dark(#d5e3ff, #0f4784);--mat-sys-secondary-fixed: light-dark(#d5e3ff, #d5e3ff);--mat-sys-secondary-fixed-dim: light-dark(#a7c8ff, #a7c8ff);--mat-sys-shadow: light-dark(#000000, #000000);--mat-sys-surface: light-dark(#fcf9f8, #131314);--mat-sys-surface-bright: light-dark(#fcf9f8, #393939);--mat-sys-surface-container: light-dark(#f0eded, #201f20);--mat-sys-surface-container-high: light-dark(#eae7e7, #2a2a2a);--mat-sys-surface-container-highest: light-dark(#e5e2e2, #393939);--mat-sys-surface-container-low: light-dark(#f6f3f3, #1c1b1c);--mat-sys-surface-container-lowest: light-dark(#ffffff, #0e0e0e);--mat-sys-surface-dim: light-dark(#dcd9d9, #131314);--mat-sys-surface-tint: light-dark(#595f65, #c1c7cd);--mat-sys-surface-variant: light-dark(#e1e2e6, #44474a);--mat-sys-tertiary: light-dark(#595f65, #c1c7cd);--mat-sys-tertiary-container: light-dark(#dde3e9, #41474d);--mat-sys-tertiary-fixed: light-dark(#dde3e9, #dde3e9);--mat-sys-tertiary-fixed-dim: light-dark(#c1c7cd, #c1c7cd);--mat-sys-neutral-variant20: #2d3134;--mat-sys-neutral10: #1c1b1c}html{--mat-sys-level0: 0px 0px 0px 0px rgba(0, 0, 0, .2), 0px 0px 0px 0px rgba(0, 0, 0, .14), 0px 0px 0px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level1: 0px 2px 1px -1px rgba(0, 0, 0, .2), 0px 1px 1px 0px rgba(0, 0, 0, .14), 0px 1px 3px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level2: 0px 3px 3px -2px rgba(0, 0, 0, .2), 0px 3px 4px 0px rgba(0, 0, 0, .14), 0px 1px 8px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level3: 0px 3px 5px -1px rgba(0, 0, 0, .2), 0px 6px 10px 0px rgba(0, 0, 0, .14), 0px 1px 18px 0px rgba(0, 0, 0, .12)}html{--mat-sys-level4: 0px 5px 5px -3px rgba(0, 0, 0, .2), 0px 8px 10px 1px rgba(0, 0, 0, .14), 0px 3px 14px 2px rgba(0, 0, 0, .12)}html{--mat-sys-level5: 0px 7px 8px -4px rgba(0, 0, 0, .2), 0px 12px 17px 2px rgba(0, 0, 0, .14), 0px 5px 22px 4px rgba(0, 0, 0, .12)}html{--mat-sys-corner-extra-large: 28px;--mat-sys-corner-extra-large-top: 28px 28px 0 0;--mat-sys-corner-extra-small: 4px;--mat-sys-corner-extra-small-top: 4px 4px 0 0;--mat-sys-corner-full: 9999px;--mat-sys-corner-large: 16px;--mat-sys-corner-large-end: 0 16px 16px 0;--mat-sys-corner-large-start: 16px 0 0 16px;--mat-sys-corner-large-top: 16px 16px 0 0;--mat-sys-corner-medium: 12px;--mat-sys-corner-none: 0;--mat-sys-corner-small: 8px}html{--mat-sys-dragged-state-layer-opacity: .16;--mat-sys-focus-state-layer-opacity: .12;--mat-sys-hover-state-layer-opacity: .08;--mat-sys-pressed-state-layer-opacity: .12}html{font-family:Google Sans,Helvetica Neue,sans-serif!important}body{height:100vh;margin:0}markdown p{margin-block-start:.5em;margin-block-end:.5em}:root{--mat-sys-primary: black;--mdc-checkbox-selected-icon-color: white;--mat-sys-background: #131314;--mat-tab-header-active-label-text-color: #8AB4F8;--mat-tab-header-active-hover-label-text-color: #8AB4F8;--mat-tab-header-active-focus-label-text-color: #8AB4F8;--mat-tab-header-label-text-weight: 500;--mdc-text-button-label-text-color: #89b4f8}:root{--mdc-dialog-container-color: #2b2b2f}:root{--mdc-dialog-subhead-color: white}:root{--mdc-circular-progress-active-indicator-color: #a8c7fa}:root{--mdc-circular-progress-size: 80}
================================================
File: src/google/adk/cli/browser/assets/audio-processor.js
================================================
/**
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.targetSampleRate = 22000;  // Change to your desired rate
        this.originalSampleRate = sampleRate; // Browser's sample rate
        this.resampleRatio = this.originalSampleRate / this.targetSampleRate;
    }
    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            let audioData = input[0]; // Get first channel's data
            if (this.resampleRatio !== 1) {
                audioData = this.resample(audioData);
            }
            this.port.postMessage(audioData);
        }
        return true; // Keep processor alive
    }
    resample(audioData) {
        const newLength = Math.round(audioData.length / this.resampleRatio);
        const resampled = new Float32Array(newLength);
        for (let i = 0; i < newLength; i++) {
            const srcIndex = Math.floor(i * this.resampleRatio);
            resampled[i] = audioData[srcIndex]; // Nearest neighbor resampling
        }
        return resampled;
    }
}
registerProcessor('audio-processor', AudioProcessor);
================================================
File: src/google/adk/cli/browser/assets/config/runtime-config.json
================================================
{
  "backendUrl": ""
}
================================================
File: src/google/adk/cli/utils/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any
from typing import Optional
from ...agents.base_agent import BaseAgent
from ...agents.llm_agent import LlmAgent
__all__ = [
    'create_empty_state',
]
def _create_empty_state(agent: BaseAgent, all_state: dict[str, Any]):
  for sub_agent in agent.sub_agents:
    _create_empty_state(sub_agent, all_state)
  if (
      isinstance(agent, LlmAgent)
      and agent.instruction
      and isinstance(agent.instruction, str)
  ):
    for key in re.findall(r'{([\w]+)}', agent.instruction):
      all_state[key] = ''
def create_empty_state(
    agent: BaseAgent, initialized_states: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
  """Creates empty str for non-initialized states."""
  non_initialized_states = {}
  _create_empty_state(agent, non_initialized_states)
  for key in initialized_states or {}:
    if key in non_initialized_states:
      del non_initialized_states[key]
  return non_initialized_states
================================================
File: src/google/adk/cli/utils/agent_loader.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import importlib
import logging
import sys
from typing import Optional
from . import envs
from ...agents.base_agent import BaseAgent
logger = logging.getLogger("google_adk." + __name__)
class AgentLoader:
  """Centralized agent loading with proper isolation, caching, and .env loading.
  Support loading agents from below folder/file structures:
  a)  {agent_name}.agent as a module name:
      agents_dir/{agent_name}/agent.py (with root_agent defined in the module)
  b)  {agent_name} as a module name
      agents_dir/{agent_name}.py (with root_agent defined in the module)
  c)  {agent_name} as a package name
      agents_dir/{agent_name}/__init__.py (with root_agent in the package)
  """
  def __init__(self, agents_dir: str):
    self.agents_dir = agents_dir.rstrip("/")
    self._original_sys_path = None
    self._agent_cache: dict[str, BaseAgent] = {}
  def _load_from_module_or_package(
      self, agent_name: str
  ) -> Optional[BaseAgent]:
    # Load for case: Import "{agent_name}" (as a package or module)
    # Covers structures:
    #   a) agents_dir/{agent_name}.py (with root_agent in the module)
    #   b) agents_dir/{agent_name}/__init__.py (with root_agent in the package)
    try:
      module_candidate = importlib.import_module(agent_name)
      # Check for "root_agent" directly in "{agent_name}" module/package
      if hasattr(module_candidate, "root_agent"):
        logger.debug("Found root_agent directly in %s", agent_name)
        if isinstance(module_candidate.root_agent, BaseAgent):
          return module_candidate.root_agent
        else:
          logger.warning(
              "Root agent found is not an instance of BaseAgent. But a type %s",
              type(module_candidate.root_agent),
          )
    except ModuleNotFoundError:
      logger.debug("Module %s itself not found.", agent_name)
      # Re-raise as ValueError to be caught by the final error message construction
      raise ValueError(
          f"Module {agent_name} not found during import attempts."
      ) from None
    except ImportError as e:
      logger.warning("Error importing %s: %s", agent_name, e)
    return None
  def _load_from_submodule(self, agent_name: str) -> Optional[BaseAgent]:
    # Load for case: Import "{agent_name}.agent" and look for "root_agent"
    # Covers structure: agents_dir/{agent_name}/agent.py (with root_agent defined in the module)
    try:
      module_candidate = importlib.import_module(f"{agent_name}.agent")
      if hasattr(module_candidate, "root_agent"):
        logger.info("Found root_agent in %s.agent", agent_name)
        if isinstance(module_candidate.root_agent, BaseAgent):
          return module_candidate.root_agent
        else:
          logger.warning(
              "Root agent found is not an instance of BaseAgent. But a type %s",
              type(module_candidate.root_agent),
          )
    except ModuleNotFoundError:
      logger.debug(
          "Module %s.agent not found, trying next pattern.", agent_name
      )
    except ImportError as e:
      logger.warning("Error importing %s.agent: %s", agent_name, e)
    return None
  def _perform_load(self, agent_name: str) -> BaseAgent:
    """Internal logic to load an agent"""
    # Add self.agents_dir to sys.path
    if self.agents_dir not in sys.path:
      sys.path.insert(0, self.agents_dir)
    logger.debug(
        "Loading .env for agent %s from %s", agent_name, self.agents_dir
    )
    envs.load_dotenv_for_agent(agent_name, str(self.agents_dir))
    if root_agent := self._load_from_submodule(agent_name):
      return root_agent
    if root_agent := self._load_from_module_or_package(agent_name):
      return root_agent
    # If no root_agent was found by any pattern
    raise ValueError(
        f"No root_agent found for '{agent_name}'. Searched in"
        f" '{agent_name}.agent.root_agent', '{agent_name}.root_agent'."
        f" Ensure '{self.agents_dir}/{agent_name}' is structured correctly,"
        " an .env file can be loaded if present, and a root_agent is"
        " exposed."
    )
  def load_agent(self, agent_name: str) -> BaseAgent:
    """Load an agent module (with caching & .env) and return its root_agent."""
    if agent_name in self._agent_cache:
      logger.debug("Returning cached agent for %s (async)", agent_name)
      return self._agent_cache[agent_name]
    logger.debug("Loading agent %s - not in cache.", agent_name)
    agent = self._perform_load(agent_name)
    self._agent_cache[agent_name] = agent
    return agent
================================================
File: src/google/adk/cli/utils/cleanup.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import logging
from typing import List
from ...runners import Runner
logger = logging.getLogger("google_adk." + __name__)
async def close_runners(runners: List[Runner]) -> None:
  cleanup_tasks = [asyncio.create_task(runner.close()) for runner in runners]
  if cleanup_tasks:
    # Wait for all cleanup tasks with timeout
    done, pending = await asyncio.wait(
        cleanup_tasks,
        timeout=30.0,  # 30 second timeout for cleanup
        return_when=asyncio.ALL_COMPLETED,
    )
    # If any tasks are still pending, log it
    if pending:
      logger.warning(
          "%s runner close tasks didn't complete in time", len(pending)
      )
      for task in pending:
        task.cancel()
================================================
File: src/google/adk/cli/utils/common.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from pydantic import alias_generators
class BaseModel(pydantic.BaseModel):
  model_config = pydantic.ConfigDict(
      alias_generator=alias_generators.to_camel,
      populate_by_name=True,
  )
================================================
File: src/google/adk/cli/utils/envs.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
import os
from dotenv import load_dotenv
logger = logging.getLogger(__file__)
def _walk_to_root_until_found(folder, filename) -> str:
  checkpath = os.path.join(folder, filename)
  if os.path.exists(checkpath) and os.path.isfile(checkpath):
    return checkpath
  parent_folder = os.path.dirname(folder)
  if parent_folder == folder:  # reached the root
    return ''
  return _walk_to_root_until_found(parent_folder, filename)
def load_dotenv_for_agent(
    agent_name: str, agent_parent_folder: str, filename: str = '.env'
):
  """Loads the .env file for the agent module."""
  # Gets the folder of agent_module as starting_folder
  starting_folder = os.path.abspath(
      os.path.join(agent_parent_folder, agent_name)
  )
  dotenv_file_path = _walk_to_root_until_found(starting_folder, filename)
  if dotenv_file_path:
    load_dotenv(dotenv_file_path, override=True, verbose=True)
    logger.info(
        'Loaded %s file for %s at %s',
        filename,
        agent_name,
        dotenv_file_path,
    )
  else:
    logger.info('No %s file found for %s', filename, agent_name)
================================================
File: src/google/adk/cli/utils/evals.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Tuple
from deprecated import deprecated
from google.genai import types as genai_types
from ...evaluation.eval_case import IntermediateData
from ...evaluation.eval_case import Invocation
from ...sessions.session import Session
@deprecated(reason='Use convert_session_to_eval_invocations instead.')
def convert_session_to_eval_format(session: Session) -> list[dict[str, Any]]:
  """Converts a session data into eval format.
  Args:
      session: The session that should be converted.
  Returns:
      list: A single evaluation dataset in the required format.
  """
  eval_case = []
  events = session.events if session and session.events else []
  for event in events:
    if event.author == 'user':
      if not event.content or not event.content.parts:
        continue
      # Extract user query
      content = event.content
      parts = content.parts
      query = parts[0].text or ''
      # Find the corresponding tool usage or response for the query
      expected_tool_use = []
      intermediate_agent_responses = []
      # Check subsequent events to extract tool uses or responses for this turn.
      for subsequent_event in events[events.index(event) + 1 :]:
        event_author = subsequent_event.author or 'agent'
        if event_author == 'user':
          # We found an event where the author was the user. This means that a
          # new turn has started. So close this turn here.
          break
        if not subsequent_event.content or not subsequent_event.content.parts:
          continue
        for subsequent_part in subsequent_event.content.parts:
          # Some events have both function call and reference
          if subsequent_part.function_call:
            tool_name = subsequent_part.function_call.name or ''
            tool_input = subsequent_part.function_call.args or {}
            expected_tool_use.append({
                'tool_name': tool_name,
                'tool_input': tool_input,
            })
          elif subsequent_part.text:
            # Also keep track of all the natural language responses that
            # agent (or sub agents) generated.
            intermediate_agent_responses.append(
                {'author': event_author, 'text': subsequent_part.text}
            )
      # If we are here then either we are done reading all the events or we
      # encountered an event that had content authored by the end-user.
      # This, basically means an end of turn.
      # We assume that the last natural language intermediate response is the
      # final response from the agent/model. We treat that as a reference.
      eval_case.append({
          'query': query,
          'expected_tool_use': expected_tool_use,
          'expected_intermediate_agent_responses': intermediate_agent_responses[
              :-1
          ],
          'reference': (
              intermediate_agent_responses[-1]['text']
              if intermediate_agent_responses
              else ''
          ),
      })
  return eval_case
def convert_session_to_eval_invocations(session: Session) -> list[Invocation]:
  """Converts a session data into a list of Invocation.
  Args:
      session: The session that should be converted.
  Returns:
      list: A list of invocation.
  """
  invocations: list[Invocation] = []
  events = session.events if session and session.events else []
  for event in events:
    if event.author == 'user':
      if not event.content or not event.content.parts:
        continue
      # The content present in this event is the user content.
      user_content = event.content
      invocation_id = event.invocation_id
      invocaton_timestamp = event.timestamp
      # Find the corresponding tool usage or response for the query
      tool_uses: list[genai_types.FunctionCall] = []
      intermediate_responses: list[Tuple[str, list[genai_types.Part]]] = []
      # Check subsequent events to extract tool uses or responses for this turn.
      for subsequent_event in events[events.index(event) + 1 :]:
        event_author = subsequent_event.author or 'agent'
        if event_author == 'user':
          # We found an event where the author was the user. This means that a
          # new turn has started. So close this turn here.
          break
        if not subsequent_event.content or not subsequent_event.content.parts:
          continue
        intermediate_response_parts = []
        for subsequent_part in subsequent_event.content.parts:
          # Some events have both function call and reference
          if subsequent_part.function_call:
            tool_uses.append(subsequent_part.function_call)
          elif subsequent_part.text:
            # Also keep track of all the natural language responses that
            # agent (or sub agents) generated.
            intermediate_response_parts.append(subsequent_part)
        if intermediate_response_parts:
          # Only add an entry if there any intermediate entries.
          intermediate_responses.append(
              (event_author, intermediate_response_parts)
          )
      # If we are here then either we are done reading all the events or we
      # encountered an event that had content authored by the end-user.
      # This, basically means an end of turn.
      # We assume that the last natural language intermediate response is the
      # final response from the agent/model. We treat that as a reference.
      invocations.append(
          Invocation(
              user_content=user_content,
              invocation_id=invocation_id,
              creation_timestamp=invocaton_timestamp,
              intermediate_data=IntermediateData(
                  tool_uses=tool_uses,
                  intermediate_responses=intermediate_responses[:-1],
              ),
              final_response=genai_types.Content(
                  parts=intermediate_responses[-1][1]
              ),
          )
      )
  return invocations
================================================
File: src/google/adk/cli/utils/logs.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import logging
import os
import tempfile
import time
LOGGING_FORMAT = (
    '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
def setup_adk_logger(level=logging.INFO):
  # Configure the root logger format and level.
  logging.basicConfig(level=level, format=LOGGING_FORMAT)
  adk_logger = logging.getLogger('google_adk')
  adk_logger.setLevel(level)
def log_to_tmp_folder(
    level=logging.INFO,
    *,
    sub_folder: str = 'agents_log',
    log_file_prefix: str = 'agent',
    log_file_timestamp: str = time.strftime('%Y%m%d_%H%M%S'),
):
  """Logs to system temp folder, instead of logging to stderr.
  Args
    sub_folder: str = 'agents_log',
    log_file_prefix: str = 'agent',
    log_file_timestamp: str = time.strftime('%Y%m%d_%H%M%S'),
  Returns
    the log file path.
  """
  log_dir = os.path.join(tempfile.gettempdir(), sub_folder)
  log_filename = f'{log_file_prefix}.{log_file_timestamp}.log'
  log_filepath = os.path.join(log_dir, log_filename)
  os.makedirs(log_dir, exist_ok=True)
  file_handler = logging.FileHandler(log_filepath, mode='w')
  file_handler.setLevel(level)
  file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
  root_logger = logging.getLogger()
  root_logger.setLevel(level)
  root_logger.handlers = []  # Clear handles to disable logging to stderr
  root_logger.addHandler(file_handler)
  print(f'Log setup complete: {log_filepath}')
  return log_filepath
================================================
File: src/google/adk/code_executors/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from .base_code_executor import BaseCodeExecutor
from .built_in_code_executor import BuiltInCodeExecutor
from .code_executor_context import CodeExecutorContext
from .unsafe_local_code_executor import UnsafeLocalCodeExecutor
logger = logging.getLogger('google_adk.' + __name__)
__all__ = [
    'BaseCodeExecutor',
    'BuiltInCodeExecutor',
    'CodeExecutorContext',
    'UnsafeLocalCodeExecutor',
]
try:
  from .vertex_ai_code_executor import VertexAiCodeExecutor
  __all__.append('VertexAiCodeExecutor')
except ImportError:
  logger.debug(
      'The Vertex sdk is not installed. If you want to use the Vertex Code'
      ' Interpreter with agents, please install it. If not, you can ignore this'
      ' warning.'
  )
try:
  from .container_code_executor import ContainerCodeExecutor
  __all__.append('ContainerCodeExecutor')
except ImportError:
  logger.debug(
      ' Executor with agents, please install it. If not, you can ignore this'
      ' warning.'
  )
================================================
File: src/google/adk/code_executors/base_code_executor.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import abc
from typing import List
from pydantic import BaseModel
from ..agents.invocation_context import InvocationContext
from .code_execution_utils import CodeExecutionInput
from .code_execution_utils import CodeExecutionResult
class BaseCodeExecutor(BaseModel):
  """Abstract base class for all code executors.
  The code executor allows the agent to execute code blocks from model responses
  and incorporate the execution results into the final response.
  Attributes:
    optimize_data_file: If true, extract and process data files from the model
      request and attach them to the code executor. Supported data file
      MimeTypes are [text/csv]. Default to False.
    stateful: Whether the code executor is stateful. Default to False.
    error_retry_attempts: The number of attempts to retry on consecutive code
      execution errors. Default to 2.
    code_block_delimiters: The list of the enclosing delimiters to identify the
      code blocks.
    execution_result_delimiters: The delimiters to format the code execution
      result.
  """
  optimize_data_file: bool = False
  """
  If true, extract and process data files from the model request
  and attach them to the code executor.
  Supported data file MimeTypes are [text/csv].
  Default to False.
  """
  stateful: bool = False
  """
  Whether the code executor is stateful. Default to False.
  """
  error_retry_attempts: int = 2
  """
  The number of attempts to retry on consecutive code execution errors. Default to 2.
  """
  code_block_delimiters: List[tuple[str, str]] = [
      ('```tool_code\n', '\n```'),
      ('```python\n', '\n```'),
  ]
  """
  The list of the enclosing delimiters to identify the code blocks.
  For example, the delimiter ('```python\n', '\n```') can be
  used to identify code blocks with the following format:
  ```python
  print("hello")
  ```
  """
  execution_result_delimiters: tuple[str, str] = ('```tool_output\n', '\n```')
  """
  The delimiters to format the code execution result.
  """
  @abc.abstractmethod
  def execute_code(
      self,
      invocation_context: InvocationContext,
      code_execution_input: CodeExecutionInput,
  ) -> CodeExecutionResult:
    """Executes code and return the code execution result.
    Args:
      invocation_context: The invocation context of the code execution.
      code_execution_input: The code execution input.
    Returns:
      The code execution result.
    """
    pass
================================================
File: src/google/adk/code_executors/built_in_code_executor.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.genai import types
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from ..models import LlmRequest
from .base_code_executor import BaseCodeExecutor
from .code_execution_utils import CodeExecutionInput
from .code_execution_utils import CodeExecutionResult
class BuiltInCodeExecutor(BaseCodeExecutor):
  """A code executor that uses the Model's built-in code executor.
  Currently only supports Gemini 2.0+ models, but will be expanded to
  other models.
  """
  @override
  def execute_code(
      self,
      invocation_context: InvocationContext,
      code_execution_input: CodeExecutionInput,
  ) -> CodeExecutionResult:
    pass
  def process_llm_request(self, llm_request: LlmRequest) -> None:
    """Pre-process the LLM request for Gemini 2.0+ models to use the code execution tool."""
    if llm_request.model and llm_request.model.startswith("gemini-2"):
      llm_request.config = llm_request.config or types.GenerateContentConfig()
      llm_request.config.tools = llm_request.config.tools or []
      llm_request.config.tools.append(
          types.Tool(code_execution=types.ToolCodeExecution())
      )
      return
    raise ValueError(
        "Gemini code execution tool is not supported for model"
        f" {llm_request.model}"
    )
================================================
File: src/google/adk/code_executors/code_execution_utils.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Utility functions for code execution."""
import base64
import binascii
import copy
import dataclasses
import re
from typing import List
from typing import Optional
from google.genai import types
@dataclasses.dataclass(frozen=True)
class File:
  """A structure that contains a file name and its content."""
  name: str
  """
  The name of the file with file extension (e.g., "file.csv").
  """
  content: str
  """
  The base64-encoded bytes of the file content.
  """
  mime_type: str = 'text/plain'
  """
  The mime type of the file (e.g., "image/png").
  """
@dataclasses.dataclass
class CodeExecutionInput:
  """A structure that contains the input of code execution."""
  code: str
  """
  The code to execute.
  """
  input_files: list[File] = dataclasses.field(default_factory=list)
  """
  The input files available to the code.
  """
  execution_id: Optional[str] = None
  """
  The execution ID for the stateful code execution.
  """
@dataclasses.dataclass
class CodeExecutionResult:
  """A structure that contains the result of code execution."""
  stdout: str = ''
  """
  The standard output of the code execution.
  """
  stderr: str = ''
  """
  The standard error of the code execution.
  """
  output_files: list[File] = dataclasses.field(default_factory=list)
  """
  The output files from the code execution.
  """
class CodeExecutionUtils:
  """Utility functions for code execution."""
  @staticmethod
  def get_encoded_file_content(data: bytes) -> bytes:
    """Gets the file content as a base64-encoded bytes.
    Args:
      data: The file content bytes.
    Returns:
      The file content as a base64-encoded bytes.
    """
    def _is_base64_encoded(data: bytes) -> bool:
      try:
        return base64.b64encode(base64.b64decode(data)) == data
      except binascii.Error:
        return False
    return data if _is_base64_encoded(data) else base64.b64encode(data)
  @staticmethod
  def extract_code_and_truncate_content(
      content: types.Content,
      code_block_delimiters: List[tuple[str, str]],
  ) -> Optional[str]:
    """Extracts the first code block from the content and truncate everything after it.
    Args:
      content: The mutable content to extract the code from.
      code_block_delimiters: The list of the enclosing delimiters to identify
        the code blocks.
    Returns:
      The first code block if found, otherwise None.
    """
    if not content or not content.parts:
      return
    # Extract the code from the executable code parts if there're no associated
    # code execution result parts.
    for idx, part in enumerate(content.parts):
      if part.executable_code and (
          idx == len(content.parts) - 1
          or not content.parts[idx + 1].code_execution_result
      ):
        content.parts = content.parts[: idx + 1]
        return part.executable_code.code
    # Extract the code from the text parts.
    text_parts = [p for p in content.parts if p.text]
    if not text_parts:
      return
    first_text_part = copy.deepcopy(text_parts[0])
    response_text = '\n'.join([p.text for p in text_parts])
    # Find the first code block.
    leading_delimiter_pattern = '|'.join(d[0] for d in code_block_delimiters)
    trailing_delimiter_pattern = '|'.join(d[1] for d in code_block_delimiters)
    pattern = re.compile(
        (
            rf'(?P<prefix>.*?)({leading_delimiter_pattern})(?P<code>.*?)({trailing_delimiter_pattern})(?P<suffix>.*?)$'
        ).encode(),
        re.DOTALL,
    )
    pattern_match = pattern.search(response_text.encode())
    if pattern_match is None:
      return
    code_str = pattern_match.group('code').decode()
    if not code_str:
      return
    content.parts = []
    if pattern_match.group('prefix'):
      first_text_part.text = pattern_match.group('prefix').decode()
      content.parts.append(first_text_part)
    content.parts.append(
        CodeExecutionUtils.build_executable_code_part(code_str)
    )
    return pattern_match.group('code').decode()
  @staticmethod
  def build_executable_code_part(code: str) -> types.Part:
    """Builds an executable code part with code string.
    Args:
      code: The code string.
    Returns:
      The constructed executable code part.
    """
    return types.Part.from_executable_code(
        code=code,
        language='PYTHON',
    )
  @staticmethod
  def build_code_execution_result_part(
      code_execution_result: CodeExecutionResult,
  ) -> types.Part:
    """Builds the code execution result part from the code execution result.
    Args:
      code_execution_result: The code execution result.
    Returns:
      The constructed code execution result part.
    """
    if code_execution_result.stderr:
      return types.Part.from_code_execution_result(
          outcome='OUTCOME_FAILED',
          output=code_execution_result.stderr,
      )
    final_result = []
    if code_execution_result.stdout or not code_execution_result.output_files:
      final_result.append(
          'Code execution result:\n' + '%s\n' % code_execution_result.stdout
      )
    if code_execution_result.output_files:
      final_result.append(
          'Saved artifacts:\n'
          + ','.join(
              ['`%s`' % f.name for f in code_execution_result.output_files]
          )
      )
    return types.Part.from_code_execution_result(
        outcome='OUTCOME_OK',
        output='\n\n'.join(final_result),
    )
  @staticmethod
  def convert_code_execution_parts(
      content: types.Content,
      code_block_delimiter: tuple[str, str],
      execution_result_delimiters: tuple[str, str],
  ):
    """Converts the code execution parts to text parts in a Content.
    Args:
      content: The mutable content to convert the code execution parts to text
        parts.
      code_block_delimiter: The delimiter to format the code block.
      execution_result_delimiters: The delimiter to format the code execution
        result.
    """
    if not content.parts:
      return
    # Handle the conversion of trailing executable code parts.
    if content.parts[-1].executable_code:
      content.parts[-1] = types.Part(
          text=(
              code_block_delimiter[0]
              + content.parts[-1].executable_code.code
              + code_block_delimiter[1]
          )
      )
    # Handle the conversion of trailing code execution result parts.
    # Skip if the Content has multiple parts, which means the Content is
    # likely generated by the model.
    elif len(content.parts) == 1 and content.parts[-1].code_execution_result:
      content.parts[-1] = types.Part(
          text=execution_result_delimiters[0]
          + content.parts[-1].code_execution_result.output
          + execution_result_delimiters[1]
      )
      content.role = 'user'
================================================
File: src/google/adk/code_executors/code_executor_context.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""The persistent context used to configure the code executor."""
import copy
import dataclasses
import datetime
from typing import Any
from typing import Optional
from ..sessions.state import State
from .code_execution_utils import File
_CONTEXT_KEY = '_code_execution_context'
_SESSION_ID_KEY = 'execution_session_id'
_INPUT_FILE_KEY = '_code_executor_input_files'
_ERROR_COUNT_KEY = '_code_executor_error_counts'
_CODE_EXECUTION_RESULTS_KEY = '_code_execution_results'
class CodeExecutorContext:
  """The persistent context used to configure the code executor."""
  _context: dict[str, Any]
  def __init__(self, session_state: State):
    """Initializes the code executor context.
    Args:
      session_state: The session state to get the code executor context from.
    """
    self._context = self._get_code_executor_context(session_state)
    self._session_state = session_state
  def get_state_delta(self) -> dict[str, Any]:
    """Gets the state delta to update in the persistent session state.
    Returns:
      The state delta to update in the persistent session state.
    """
    context_to_update = copy.deepcopy(self._context)
    return {_CONTEXT_KEY: context_to_update}
  def get_execution_id(self) -> Optional[str]:
    """Gets the session ID for the code executor.
    Returns:
      The session ID for the code executor context.
    """
    if _SESSION_ID_KEY not in self._context:
      return None
    return self._context[_SESSION_ID_KEY]
  def set_execution_id(self, session_id: str):
    """Sets the session ID for the code executor.
    Args:
      session_id: The session ID for the code executor.
    """
    self._context[_SESSION_ID_KEY] = session_id
  def get_processed_file_names(self) -> list[str]:
    """Gets the processed file names from the session state.
    Returns:
      A list of processed file names in the code executor context.
    """
      return []
  def add_processed_file_names(self, file_names: [str]):
    """Adds the processed file name to the session state.
    Args:
      file_names: The processed file names to add to the session state.
    """
  def get_input_files(self) -> list[File]:
    """Gets the code executor input file names from the session state.
    Returns:
      A list of input files in the code executor context.
    """
    if _INPUT_FILE_KEY not in self._session_state:
      return []
    return [File(**file) for file in self._session_state[_INPUT_FILE_KEY]]
  def add_input_files(
      self,
      input_files: list[File],
  ):
    """Adds the input files to the code executor context.
    Args:
      input_files: The input files to add to the code executor context.
    """
    if _INPUT_FILE_KEY not in self._session_state:
      self._session_state[_INPUT_FILE_KEY] = []
    for input_file in input_files:
      self._session_state[_INPUT_FILE_KEY].append(
          dataclasses.asdict(input_file)
      )
  def clear_input_files(self):
    """Removes the input files and processed file names to the code executor context."""
    if _INPUT_FILE_KEY in self._session_state:
      self._session_state[_INPUT_FILE_KEY] = []
  def get_error_count(self, invocation_id: str) -> int:
    """Gets the error count from the session state.
    Args:
      invocation_id: The invocation ID to get the error count for.
    Returns:
      The error count for the given invocation ID.
    """
    if _ERROR_COUNT_KEY not in self._session_state:
      return 0
    return self._session_state[_ERROR_COUNT_KEY].get(invocation_id, 0)
  def increment_error_count(self, invocation_id: str):
    """Increments the error count from the session state.
    Args:
      invocation_id: The invocation ID to increment the error count for.
    """
    if _ERROR_COUNT_KEY not in self._session_state:
      self._session_state[_ERROR_COUNT_KEY] = {}
    self._session_state[_ERROR_COUNT_KEY][invocation_id] = (
        self.get_error_count(invocation_id) + 1
    )
  def reset_error_count(self, invocation_id: str):
    """Resets the error count from the session state.
    Args:
      invocation_id: The invocation ID to reset the error count for.
    """
    if _ERROR_COUNT_KEY not in self._session_state:
      return
    if invocation_id in self._session_state[_ERROR_COUNT_KEY]:
      del self._session_state[_ERROR_COUNT_KEY][invocation_id]
  def update_code_execution_result(
      self,
      invocation_id: str,
      code: str,
      result_stdout: str,
      result_stderr: str,
  ):
    """Updates the code execution result.
    Args:
      invocation_id: The invocation ID to update the code execution result for.
      code: The code to execute.
      result_stdout: The standard output of the code execution.
      result_stderr: The standard error of the code execution.
    """
    if _CODE_EXECUTION_RESULTS_KEY not in self._session_state:
      self._session_state[_CODE_EXECUTION_RESULTS_KEY] = {}
    if invocation_id not in self._session_state[_CODE_EXECUTION_RESULTS_KEY]:
      self._session_state[_CODE_EXECUTION_RESULTS_KEY][invocation_id] = []
    self._session_state[_CODE_EXECUTION_RESULTS_KEY][invocation_id].append({
        'code': code,
        'result_stdout': result_stdout,
        'result_stderr': result_stderr,
        'timestamp': int(datetime.datetime.now().timestamp()),
    })
  def _get_code_executor_context(self, session_state: State) -> dict[str, Any]:
    """Gets the code executor context from the session state.
    Args:
      session_state: The session state to get the code executor context from.
    Returns:
      A dict of code executor context.
    """
    if _CONTEXT_KEY not in session_state:
      session_state[_CONTEXT_KEY] = {}
    return session_state[_CONTEXT_KEY]
================================================
File: src/google/adk/code_executors/container_code_executor.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import atexit
import os
from typing import Optional
from pydantic import Field
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from .base_code_executor import BaseCodeExecutor
from .code_execution_utils import CodeExecutionInput
from .code_execution_utils import CodeExecutionResult
class ContainerCodeExecutor(BaseCodeExecutor):
  """A code executor that uses a custom container to execute code.
  Attributes:
    image: The tag of the predefined image or custom image to run on the
  """
  base_url: Optional[str] = None
  """
  """
  image: str = None
  """
  The tag of the predefined image or custom image to run on the container.
  """
  """
  """
  # Overrides the BaseCodeExecutor attribute: this executor cannot be stateful.
  stateful: bool = Field(default=False, frozen=True, exclude=True)
  # Overrides the BaseCodeExecutor attribute: this executor cannot
  # optimize_data_file.
  optimize_data_file: bool = Field(default=False, frozen=True, exclude=True)
  _container: Container = None
  def __init__(
      self,
      base_url: Optional[str] = None,
      image: Optional[str] = None,
      **data,
  ):
    """Initializes the ContainerCodeExecutor.
    Args:
      image: The tag of the predefined image or custom image to run on the
      **data: The data to initialize the ContainerCodeExecutor.
    """
      raise ValueError(
      )
    if 'stateful' in data and data['stateful']:
      raise ValueError('Cannot set `stateful=True` in ContainerCodeExecutor.')
    if 'optimize_data_file' in data and data['optimize_data_file']:
      raise ValueError(
          'Cannot set `optimize_data_file=True` in ContainerCodeExecutor.'
      )
    super().__init__(**data)
    self.base_url = base_url
    self.image = image if image else DEFAULT_IMAGE_TAG
    self._client = (
        if not self.base_url
    )
    # Initialize the container.
    self.__init_container()
    # Close the container when the on exit.
    atexit.register(self.__cleanup_container)
  @override
  def execute_code(
      self,
      invocation_context: InvocationContext,
      code_execution_input: CodeExecutionInput,
  ) -> CodeExecutionResult:
    output = ''
    error = ''
    exec_result = self._container.exec_run(
        ['python3', '-c', code_execution_input.code],
        demux=True,
    )
    if exec_result.output and exec_result.output[0]:
      output = exec_result.output[0].decode('utf-8')
    if (
        exec_result.output
        and len(exec_result.output) > 1
        and exec_result.output[1]
    ):
      error = exec_result.output[1].decode('utf-8')
    # Collect the final result.
    return CodeExecutionResult(
        stdout=output,
        stderr=error,
        output_files=[],
    )
    self._client.images.build(
        tag=self.image,
        rm=True,
    )
  def _verify_python_installation(self):
    """Verifies the container has python3 installed."""
    exec_result = self._container.exec_run(['which', 'python3'])
    if exec_result.exit_code != 0:
      raise ValueError('python3 is not installed in the container.')
  def __init_container(self):
    """Initializes the container."""
    if not self._client:
    print('Starting container for ContainerCodeExecutor...')
    self._container = self._client.containers.run(
        image=self.image,
        detach=True,
        tty=True,
    )
    print(f'Container {self._container.id} started.')
    # Verify the container is able to run python3.
    self._verify_python_installation()
  def __cleanup_container(self):
    """Closes the container on exit."""
    if not self._container:
      return
    print('[Cleanup] Stopping the container...')
    self._container.stop()
    self._container.remove()
    print(f'Container {self._container.id} stopped and removed.')
================================================
File: src/google/adk/code_executors/unsafe_local_code_executor.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from contextlib import redirect_stdout
import io
import re
from typing import Any
from pydantic import Field
from typing_extensions import override
from ..agents.invocation_context import InvocationContext
from .base_code_executor import BaseCodeExecutor
from .code_execution_utils import CodeExecutionInput
from .code_execution_utils import CodeExecutionResult
def _prepare_globals(code: str, globals_: dict[str, Any]) -> None:
  """Prepare globals for code execution, injecting __name__ if needed."""
  if re.search(r"if\s+__name__\s*==\s*['\"]__main__['\"]", code):
    globals_['__name__'] = '__main__'
class UnsafeLocalCodeExecutor(BaseCodeExecutor):
  """A code executor that unsafely execute code in the current local context."""
  # Overrides the BaseCodeExecutor attribute: this executor cannot be stateful.
  stateful: bool = Field(default=False, frozen=True, exclude=True)
  # Overrides the BaseCodeExecutor attribute: this executor cannot
  # optimize_data_file.
  optimize_data_file: bool = Field(default=False, frozen=True, exclude=True)
  def __init__(self, **data):
    """Initializes the UnsafeLocalCodeExecutor."""
    if 'stateful' in data and data['stateful']:
      raise ValueError('Cannot set `stateful=True` in UnsafeLocalCodeExecutor.')
    if 'optimize_data_file' in data and data['optimize_data_file']:
      raise ValueError(
          'Cannot set `optimize_data_file=True` in UnsafeLocalCodeExecutor.'
      )
    super().__init__(**data)
  @override
  def execute_code(
      self,
      invocation_context: InvocationContext,
      code_execution_input: CodeExecutionInput,
  ) -> CodeExecutionResult:
    # Execute the code.
    output = ''
    error = ''
    try:
      globals_ = {}
      _prepare_globals(code_execution_input.code, globals_)
      locals_ = {}
      stdout = io.StringIO()
      with redirect_stdout(stdout):
        exec(code_execution_input.code, globals_, locals_)
      output = stdout.getvalue()
    except Exception as e:
      error = str(e)
    # Collect the final result.
    return CodeExecutionResult(
        stdout=output,
        stderr=error,
        output_files=[],
    )
================================================
File: src/google/adk/code_executors/vertex_ai_code_executor.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import mimetypes
import os
from typing import Any
from typing import Optional
from typing_extensions import override
from vertexai.preview.extensions import Extension
from ..agents.invocation_context import InvocationContext
from .base_code_executor import BaseCodeExecutor
from .code_execution_utils import CodeExecutionInput
from .code_execution_utils import CodeExecutionResult
from .code_execution_utils import File
_SUPPORTED_IMAGE_TYPES = ['png', 'jpg', 'jpeg']
_SUPPORTED_DATA_FILE_TYPES = ['csv']
_IMPORTED_LIBRARIES = '''
import io
import math
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
def crop(s: str, max_chars: int = 64) -> str:
  """Crops a string to max_chars characters."""
  return s[: max_chars - 3] + '...' if len(s) > max_chars else s
def explore_df(df: pd.DataFrame) -> None:
  """Prints some information about a pandas DataFrame."""
  with pd.option_context(
      'display.max_columns', None, 'display.expand_frame_repr', False
  ):
    # Print the column names to never encounter KeyError when selecting one.
    df_dtypes = df.dtypes
    # Obtain information about data types and missing values.
    df_nulls = (len(df) - df.isnull().sum()).apply(
        lambda x: f'{x} / {df.shape[0]} non-null'
    )
    # Explore unique total values in columns using `.unique()`.
    df_unique_count = df.apply(lambda x: len(x.unique()))
    # Explore unique values in columns using `.unique()`.
    df_unique = df.apply(lambda x: crop(str(list(x.unique()))))
    df_info = pd.concat(
        (
            df_dtypes.rename('Dtype'),
            df_nulls.rename('Non-Null Count'),
            df_unique_count.rename('Unique Values Count'),
            df_unique.rename('Unique Values'),
        ),
        axis=1,
    )
    df_info.index.name = 'Columns'
    print(f"""Total rows: {df.shape[0]}
Total columns: {df.shape[1]}
{df_info}""")
'''
def _get_code_interpreter_extension(resource_name: str = None):
  """Returns: Load or create the code interpreter extension."""
  if not resource_name:
  if resource_name:
    new_code_interpreter = Extension(resource_name)
  else:
    new_code_interpreter = Extension.from_hub('code_interpreter')
        new_code_interpreter.gca_resource.name
    )
  return new_code_interpreter
class VertexAiCodeExecutor(BaseCodeExecutor):
  """A code executor that uses Vertex Code Interpreter Extension to execute code.
  Attributes:
    resource_name: If set, load the existing resource name of the code
      interpreter extension instead of creating a new one. Format:
      projects/123/locations/us-central1/extensions/456
  """
  resource_name: str = None
  """
  If set, load the existing resource name of the code interpreter extension
  instead of creating a new one.
  Format: projects/123/locations/us-central1/extensions/456
  """
  _code_interpreter_extension: Extension
  def __init__(
      self,
      resource_name: str = None,
      **data,
  ):
    """Initializes the VertexAiCodeExecutor.
    Args:
      resource_name: If set, load the existing resource name of the code
        interpreter extension instead of creating a new one. Format:
        projects/123/locations/us-central1/extensions/456
      **data: Additional keyword arguments to be passed to the base class.
    """
    super().__init__(**data)
    self.resource_name = resource_name
    self._code_interpreter_extension = _get_code_interpreter_extension(
        self.resource_name
    )
  @override
  def execute_code(
      self,
      invocation_context: InvocationContext,
      code_execution_input: CodeExecutionInput,
  ) -> CodeExecutionResult:
    # Execute the code.
    code_execution_result = self._execute_code_interpreter(
        self._get_code_with_imports(code_execution_input.code),
        code_execution_input.input_files,
        code_execution_input.execution_id,
    )
    # Save output file as artifacts.
    saved_files = []
    file_count = 0
    for output_file in code_execution_result['output_files']:
      file_type = output_file['name'].split('.')[-1]
      if file_type in _SUPPORTED_IMAGE_TYPES:
        file_count += 1
        saved_files.append(
            File(
                name=output_file['name'],
                content=output_file['contents'],
                mime_type=f'image/{file_type}',
            )
        )
      elif file_type in _SUPPORTED_DATA_FILE_TYPES:
        file_count += 1
        saved_files.append(
            File(
                name=output_file['name'],
                content=output_file['contents'],
                mime_type=f'text/{file_type}',
            )
        )
      else:
        mime_type, _ = mimetypes.guess_type(output_file['name'])
        saved_files.append(
            File(
                name=output_file['name'],
                content=output_file['contents'],
                mime_type=mime_type,
            )
        )
    # Collect the final result.
    return CodeExecutionResult(
        stdout=code_execution_result.get('execution_result', ''),
        stderr=code_execution_result.get('execution_error', ''),
        output_files=saved_files,
    )
  def _execute_code_interpreter(
      self,
      code: str,
      input_files: Optional[list[File]] = None,
      session_id: Optional[str] = None,
  ) -> dict[str, Any]:
    """Executes the code interpreter extension.
    Args:
      code: The code to execute.
      input_files: The input files to execute the code with.
      session_id: The session ID to execute the code with.
    Returns:
      The response from the code interpreter extension.
    """
    operation_params = {'code': code}
    if input_files:
      operation_params['files'] = [
          {'name': f.name, 'contents': f.content} for f in input_files
      ]
    if session_id:
      operation_params['session_id'] = session_id
    response = self._code_interpreter_extension.execute(
        operation_id='execute',
        operation_params=operation_params,
    )
    return response
  def _get_code_with_imports(self, code: str) -> str:
    """Builds the code string with built-in imports.
    Args:
      code: The code to execute.
    Returns:
      The code string with built-in imports.
    """
    return f"""
{_IMPORTED_LIBRARIES}
{code}
"""
================================================
File: src/google/adk/evaluation/__init__.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
logger = logging.getLogger('google_adk.' + __name__)
__all__ = []
try:
  from .agent_evaluator import AgentEvaluator
  __all__.append('AgentEvaluator')
except ImportError:
  logger.debug(
      'The Vertex[eval] sdk is not installed. If you want to use the Vertex'
      ' Evaluation with agents, please install it(pip install'
      ' "google-cloud-aiplatform[evaluation]). If not, you can ignore this'
      ' warning.'
  )
================================================
File: src/google/adk/evaluation/agent_evaluator.py
================================================
#
# you may not use this file except in compliance with the License.
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
import logging
import os
from os import path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
import uuid
from pydantic import ValidationError
from .eval_set import EvalSet
from .evaluation_generator import EvaluationGenerator
from .evaluator import EvalStatus
from .evaluator import EvaluationResult
from .evaluator import Evaluator
from .local_eval_sets_manager import convert_eval_set_to_pydanctic_schema
from .response_evaluator import ResponseEvaluator
from .trajectory_evaluator import TrajectoryEvaluator
logger = logging.getLogger("google_adk." + __name__)
# Constants for default runs and evaluation criteria
NUM_RUNS = 2
TOOL_TRAJECTORY_SCORE_KEY = "tool_trajectory_avg_score"
# This evaluation is not very stable.
# This is always optional unless explicitly specified.
RESPONSE_EVALUATION_SCORE_KEY = "response_evaluation_score"
RESPONSE_MATCH_SCORE_KEY = "response_match_score"
ALLOWED_CRITERIA = [
    TOOL_TRAJECTORY_SCORE_KEY,
    RESPONSE_EVALUATION_SCORE_KEY,
    RESPONSE_MATCH_SCORE_KEY,
]
QUERY_COLUMN = "query"
REFERENCE_COLUMN = "reference"
EXPECTED_TOOL_USE_COLUMN = "expected_tool_use"
DEFAULT_CRITERIA = {
    TOOL_TRAJECTORY_SCORE_KEY: 1.0,  # 1-point scale; 1.0 is perfect.
    RESPONSE_MATCH_SCORE_KEY: 0.8,  # Rouge-1 text match; 0.8 is default.
}
def load_json(file_path: str) -> Union[Dict, List]:
  with open(file_path, "r") as f:
    return json.load(f)
class AgentEvaluator:
  @staticmethod
    if os.path.exists(config_path):
      config_data = load_json(config_path)
      if "criteria" in config_data and isinstance(
          config_data["criteria"], dict
      ):
        return config_data["criteria"]
      else:
        raise ValueError(
            " 'criteria' dictionary."
        )
    return DEFAULT_CRITERIA
  @staticmethod
  async def evaluate_eval_set(
      agent_module: str,
      eval_set: EvalSet,
      criteria: dict[str, float],
      num_runs=NUM_RUNS,
      agent_name=None,
  ):
    """Evaluates an agent using the given EvalSet.
    Args:
      agent_module: The path to python module that contains the definition of
        the agent. There is convention in place here, where the code is going to
        look for 'root_agent' in the loaded module.
      eval_set: The eval set.
      criteria: Evauation criterias, a dictionary of metric names to their
        respective thresholds.
      num_runs: Number of times all entries in the eval dataset should be
        assessed.
      agent_name: The name of the agent.
    """
    eval_case_responses_list = await EvaluationGenerator.generate_responses(
        eval_set=eval_set,
        agent_module_path=agent_module,
        repeat_num=num_runs,
        agent_name=agent_name,
    )
    for eval_case_responses in eval_case_responses_list:
      actual_invocations = [
          invocation
          for invocations in eval_case_responses.responses
          for invocation in invocations
      ]
      expected_invocations = (
          eval_case_responses.eval_case.conversation * num_runs
      )
      for metric_name, threshold in criteria.items():
        metric_evaluator = AgentEvaluator._get_metric_evaluator(
            metric_name=metric_name, threshold=threshold
        )
        evaluation_result: EvaluationResult = (
            metric_evaluator.evaluate_invocations(
                actual_invocations=actual_invocations,
                expected_invocations=expected_invocations,
            )
        )
        assert evaluation_result.overall_eval_status == EvalStatus.PASSED, (
            f"{metric_name} for {agent_module} Failed. Expected {threshold},"
            f" but got {evaluation_result.overall_score}."
        )
  @staticmethod
  async def evaluate(
      agent_module: str,
      eval_dataset_file_path_or_dir: str,
      num_runs: int = NUM_RUNS,
      agent_name: Optional[str] = None,
      initial_session_file: Optional[str] = None,
  ):
    """Evaluates an Agent given eval data.
    Args:
      agent_module: The path to python module that contains the definition of
        the agent. There is convention in place here, where the code is going to
        look for 'root_agent' in the loaded module.
      eval_dataset_file_path_or_dir: The eval data set. This can be either a string representing
        full path to the file containing eval dataset, or a directory that is
      num_runs: Number of times all entries in the eval dataset should be
        assessed.
      agent_name: The name of the agent.
      initial_session_file: File that contains initial session state that is
        needed by all the evals in the eval dataset.
    """
    if isinstance(eval_dataset_file_path_or_dir, str) and os.path.isdir(
        eval_dataset_file_path_or_dir
    ):
      for root, _, files in os.walk(eval_dataset_file_path_or_dir):
        for file in files:
    else:
    initial_session = AgentEvaluator._get_initial_session(initial_session_file)
      eval_set = AgentEvaluator._load_eval_set_from_file(
      )
      await AgentEvaluator.evaluate_eval_set(
          agent_module=agent_module,
          eval_set=eval_set,
          criteria=criteria,
          num_runs=num_runs,
          agent_name=agent_name,
      )
  @staticmethod
