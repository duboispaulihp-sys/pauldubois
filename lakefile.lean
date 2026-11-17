import Lake
open Lake DSL

package «gerver-sofa» where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib «GerverSofa»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "15cf10d19dfd4cdee9602318e271fa3ce99c454d"
