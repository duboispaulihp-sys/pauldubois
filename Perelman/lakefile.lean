import Lake
open Lake DSL

package «Perelman» where
  version := v!"0.1.0"
  description := "Statement-and-reduction scaffold of Perelman's three arXiv manuscripts (math/0211159, math/0303109, math/0307245), unified as a single Lean document."

@[default_target]
lean_lib «Perelman»
