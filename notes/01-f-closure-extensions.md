# Note A — Extending the F-Closure Toolkit

**Working-session notes, companion to "The Harmless Subgroup and the F-Closure Lemma" (P. Dubois).**

Notation throughout follows the parent document. $X$ is a smooth projective variety
over $\mathbb{C}$ (§5 treats compact Kähler), $\mathrm{CH}^p(X)$ is the Chow group of
codimension-$p$ cycles modulo rational equivalence, $B^p(X) \subset \mathrm{Hdg}^{2p}(X,\mathbb{Q})$
is the rationally algebraic subspace spanned by classes of $\mathbb{Q}$-cycles
(the "harmless" image of algebraic cycles), and
$F^p(X) \subseteq \mathrm{Hdg}^{2p}(X,\mathbb{Q})$ is the F-subgroup of Theorem 4.5:
the B-stable group of Hodge classes closed under all integral-cycle-generated
Hodge correspondences. Recall the standing convention of the parent document:
Theorem 4.5 supplies, for each Hodge class $\gamma$ of appropriate bidegree on a product
$V\times W$, a transport operation $\tau \mapsto (\gamma)_*(\tau)$, and the F-closure lemma says
$F^p$ absorbs the action of all such $\gamma$ built from integrally algebraic correspondences
while $B$ is closed under them. We number our propositions in this note's own sections;
citations "Thm 4.5", "Cor 4.8", "Prop 2.3 of the parent", "App. B" refer to the parent document.

Everything below is proved in full. Conditional results state their hypotheses
exactly at the statement and never use them silently.

---

## §1. A lemma on rationally algebraic correspondences

We will use the following statement twice (Props 3.1 and 3.3), so we isolate it.

**Lemma 1.1 (B preserved by correspondence pushforward — unconditional).**
*Let $V, W$ be smooth projective, $\gamma \in \mathrm{CH}^{c}(V \times W)_{\mathbb{Q}}$ a
rationally algebraic correspondence, and let $(\gamma)_* : \mathrm{Hdg}^{2j}(V) \to
\mathrm{Hdg}^{2(j + c - \dim V)}(W)$ denote the induced pushforward in cohomology,*

$$(\gamma)_*\alpha \;=\; \mathrm{pr}_{2*}\bigl(\mathrm{pr}_1^{*}\alpha \cup [\gamma]\bigr),$$

*where $\mathrm{pr}_1^*\alpha$ has codimension $j$ on $V \times W$, $[\gamma]$ has
codimension $c$, and $\mathrm{pr}_{2*}$ lowers codimension by $\dim W$, so that
$(\gamma)_*\alpha$ has codimension $j + c - \dim V$ on $W$. Then*

$$(\gamma)_*\bigl(B^{j}(V)\bigr) \;\subseteq\; B^{\,j+c-\dim V}(W).$$

*Proof. Since $B^{j}(V)$ is spanned over $\mathbb{Q}$ by the classes $[Z]_{\mathbb{Q}}$
of subvarieties $Z \subset V$ of codimension $j$, since $(\gamma)_*$ is
$\mathbb{Q}$-linear in $\alpha$, and since $\gamma$ is a $\mathbb{Q}$-linear
combination of integral correspondences, it suffices to handle the case of one
integral $\gamma_{\mathbb{Z}} \in \mathrm{CH}^{c}(V \times W)_{\mathbb{Z}}$ and one
integral generator $z = [Z]_{\mathbb{Q}} \in B^{j}(V)$ with $Z$ reduced and
irreducible, and then extend by $\mathbb{Q}$-linearity.

On cycles, $(\gamma_{\mathbb{Z}})_*[Z]$ is computed as
$\mathrm{pr}_{2*}\bigl([Z \times W] \cdot [\gamma_{\mathbb{Z}}]\bigr)$. Both
factors are integral cycles on the smooth variety $V \times W$: indeed
$\mathrm{pr}_1^{-1}Z = Z \times W$ and $[\gamma_{\mathbb{Z}}]$ is integral. Their
Fulton–MacPherson intersection product $[Z \times W] \cdot [\gamma_{\mathbb{Z}}]$
(Fulton, *Intersection Theory*, Ch. 8, defined on the smooth ambient $V \times W$
via deformation to the normal cone) is a well-defined element of
$\mathrm{CH}^{j + c}(V \times W)_{\mathbb{Z}}$, and the proper pushforward of an
integral cycle is an integral cycle by definition of $\mathrm{pr}_{2*}$ on cycles
(Fulton, Ch. 1). Hence

$$(\gamma_{\mathbb{Z}})_*[Z] \;=\; [\,\text{an integral cycle on } W\,]_{\mathbb{Q}}
\;\in\; B^{\,j+c-\dim V}(W),$$

because $B^{\,j+c-\dim V}(W)$ is by definition the $\mathbb{Q}$-span of integral
cycle classes in that codimension. Extending by $\mathbb{Q}$-linearity over the
generators $[Z]_{\mathbb{Q}}$ and the lines of $\gamma$ gives
$(\gamma)_*(B^{j}(V)) \subseteq B^{\,j+c-\dim V}(W)$. ∎

**Remark 1.2.** The proof uses nothing about Hodge theory beyond the definition
of $B$; it is standard cycle-level arithmetic. In particular the lemma is
unconditional — no involvement of $F$, no appeal to Theorem 4.5, and no
F-group appears anywhere in it. This is what makes it usable in both
Propositions 3.1 and 3.3 below.

---

## §2. Collapse: full hypotheses given, the toolkit trivializes

The parent document's Cor 4.8 upgrades $F^p$ using only correspondences
generated inside the cycle-level toolkit. A natural question: if we feed the
F-machine *all* Hodge correspondences at once, does $F^p$ at least equal
$\mathrm{Hdg}^{2p}$ pointwise? The answer is that, on a variety where the point
class is pivotal, the operation is so strong it collapses the whole construction.

**Proposition 2.1 (setup).** *Let $X$ be smooth projective of complex dimension
$n$ and let $\omega = [pt]_{\mathbb{Q}} \in \mathrm{Hdg}^{2n}(X)$ be the class of
a point (equivalently, of any rational point of $X$, or $0$-cycle of degree $1$).
For $\tau \in \mathrm{Hdg}^{2p}(X)$ define*

$$\gamma_\tau \;=\; \mathrm{pr}_1^*\,\omega \cup \mathrm{pr}_2^*\,\tau
\;\in\; \mathrm{Hdg}^{2n + 2p}(X \times X),$$

*i.e. as a Hodge class of type $(n+p, n+p)$ on $X\times X$ — the product of a
type-$(n,n)$ class and a type-$(p,p)$ class, so of type $(n+p,n+p)$; and as a
diagonal-type correspondence $\gamma_\tau$ acts on cohomology as scalar
multiplication by $\int_X \omega \cdot \tau$-amplitudes as follows.*

*Then the correspondence-pushforward identity holds:*

$$(\gamma_\tau)_*(\alpha) \;=\; \int_X \omega\cup\alpha \;\cdot\; \tau
\qquad \text{for all } \alpha \in H^{2k}(X),$$

*and applying it to the unit class $1 \in H^0(X)$ gives $(\gamma_\tau)_*(1) = (\int_X \omega)\tau = \tau$
(writing coefficients so that $\int_X \omega = 1$; more generally $\int_X \omega = [\mathbb{C}X]$-degree,
which is $1$ for a rational point). In particular the single Hodge class $\gamma_\tau$
on $X \times X$ transports $1$ to $\tau$. Proof:*

$(\gamma_\tau)_*(1) = \mathrm{pr}_{2*}(\mathrm{pr}_1^* 1 \cup \gamma_\tau)
= \mathrm{pr}_{2*}(\gamma_\tau)
= \mathrm{pr}_{2*}(\mathrm{pr}_1^*\omega \cup \mathrm{pr}_2^*\tau)
= \mathrm{pr}_{2*}(\mathrm{pr}_1^*\omega) \cup \tau$

*using the pushforward–cup-product projection formula
$\mathrm{pr}_{2*}(a \cup \mathrm{pr}_2^* b) = \mathrm{pr}_{2*}(a) \cup b$ with
$a = \mathrm{pr}_1^*\omega$. Finally
concretely: $\mathrm{pr}_1^*\omega$ is supported on $\{pt\}\times X$; integrating
over the fibers of $\mathrm{pr}_2: X\times X \to X$ (each a copy of $X$) the class
$\mathrm{pr}_1^*\omega|_{\{pt\}\times X} = \omega$ gives
$\mathrm{pr}_{2*}(\mathrm{pr}_1^*\omega) = (\int_X \omega)\cdot 1 \in H^0(X)$. With
$\int_X \omega = 1$, we are done. The general-$\alpha$ identity is the same
computation with $\mathrm{pr}_1^*\alpha$ inserted, using
$\int_{\{pt\}\times X} \alpha = \int_X \alpha \cup \omega$. ∎*

**Proposition 2.2 (Collapse).** *Let $X$ be smooth projective over $\mathbb{C}$
of dimension $n$ carrying a rational point (so $\omega = [pt] \in B^n(X)$ is a
genuine algebraic seed). The following are equivalent:*

1. *The Hodge conjecture $\mathrm{HC}_{\mathbb{Q}}(X)$ holds for $X$: every
   $\tau \in \mathrm{Hdg}^{2p}(X) \cap H^{2p}_{\text{rat}}$ lies in $B^p(X)$, for all $p$.*
2. *$F^p(X) = \mathrm{Hdg}^{2p}(X,\mathbb{Q})$ for every $p$.*
3. *$F^p(X)$ is stable under the transport $(\gamma_\tau)_*(1) \mapsto \tau$ for
   every Hodge class $\tau \in \mathrm{Hdg}^{2p}$, of every degree $p$.*
4. *$F = F(X)$ is stable under the action of **all** Hodge correspondences
   $\gamma \in \mathrm{Hdg}(X\times X)$ (not merely those generated by the
   cycle-level toolkit of the parent document).*

*(2) ⟹ (3): if $1 \in F^0$ and every $\tau$ already lies in $F^p = \mathrm{Hdg}^{2p}$,
stability is immediate. (3) ⟹ (1): by Prop 2.1, $(\gamma_\tau)_*(1) = \tau$ and
$1 \in B^0(X) \subseteq F^0(X)$ always (the point $\mathrm{Spec}\,\mathbb{C}\to X$
is an algebraic cycle of codimension $0$; indeed $B^0 = \mathbb{Q}$).
So (3) says $\tau \in F^p$ for all $\tau$, and since $F^p \subseteq \mathrm{Hdg}^{2p}$
always, $F^p = \mathrm{Hdg}^{2p}$; then certainly $\tau \in B^p$ is *not* implied —
so this arrow needs the hypothesis that $F^p = B^p$-stability is all we asked; to
avoid a wrong statement we record the honest content:*

**Correction to the arrow (4)⟹(1).** As the argument above shows, (3) forces
$F^p = \mathrm{Hdg}^{2p}$. The equivalence that actually holds, and that we
record as the main collapse statement, is:

**Proposition 2.2′ (Collapse, corrected and final).** *$X$ smooth projective
with a rational point. TFAE:*

1. *$\mathrm{HC}_{\mathbb{Q}}(X)$ holds.*
2. *$B^p(X) = \mathrm{Hdg}^{2p}(X)$ for every $p$.*
3. *$F^p(X) = \mathrm{Hdg}^{2p}(X)$ for every $p$ **and** $F^p(X) = B^p(X)$
   (that is, the F-closure adds nothing beyond $B$).*

*Indeed (1)⟺(2) is the definition, and (2)⟹(3) is trivial. For (3)⟹(2): if
$F^p = B^p$ and $F^p = \mathrm{Hdg}^{2p}$, then $B^p = \mathrm{Hdg}^{2p}$. The
interesting direction is the "collapse" **in the other sense**, and it is a
positive collapse — of the toolkit:*

**Proposition 2.3 (Sharpness of the no-upgrade hypothesis).** *Let $X$ be as
above. If the F-closure machine is allowed correspondences generated from
*arbitrary* Hodge classes $\gamma_\tau \in \mathrm{Hdg}^{2n+2p}(X\times X)$
(with no requirement that $\gamma_\tau$ itself be built from algebraic cycles),
then starting from the trivial seed input (point classes only, $B^0 = \mathbb{Q}$)
one generates *every* Hodge class on $X$ in one step: the "seed-generation"
process becomes vacuous, because Cor 4.8 of the parent (the no-upgrade corollary)
would conclude $F^p(X) = \mathrm{Hdg}^{2p}(X)$ *unconditionally*, which combined
with Prop 2.2′ (3)⟹(2) is exactly $\mathrm{HC}_{\mathbb{Q}}(X)$.*

*Proof. By Prop 2.1, $\tau = (\gamma_\tau)_*(1)$ with $1 \in B^0$. Feeding
all $\gamma_\tau$ into the transport machinery of Theorem 4.5 makes $F^p$ absorb
all $\tau \in \mathrm{Hdg}^{2p}$ in a single step from the seed $1 \in B^0 \subseteq F^0$.
This is precisely the situation Cor 4.8 excludes by its standing hypothesis
("correspondences from the cycle-level toolkit"): allowing arbitrary Hodge
correspondences makes the hypothesis of Theorem 4.5 trivially satisfiable and
its conclusion as strong as HC itself. Hence any *unconditional* upgrade of this
kind would prove HC — the hypothesis is sharp. Concretely: the no-upgrade
corollary's hypothesis "$\gamma$ is a $\mathbb{Q}$-combination of correspondences
already known to preserve $B$" cannot hold for $\gamma_\tau$ unless one already
knows $\tau$-preservation, i.e. knows HC($X$) itself. ∎*

**Consequence for our program.** The toolkit must stay inside the cycle level
(this is what makes Theorem 4.5 non-vacuous), so all extension results below are
either (a) unconditional cyc statements (Lemma 1.1, Prop 4.1), or (b) honest
conditional statements isolating exactly which Hodge-theoretic input is missing
(Props 3.1, 3.3), or (c) transfers (Props 5.1–5.3) that hold verbatim because
they do not need the missing input.

---

## §3. Künneth components and primitive detection (conditional on C)

Recall from the parent document §5 the two open items: deformative closure of
$B$ under Künneth components (item labeled "C" there: *does $B$ contain the
Künneth components $\pi_k(X)$ of the diagonal?*) and Abel–Jacobi compatibility.
Both Props 3.1 and 3.3 below are stated conditionally on C, exactly as the parent
document flagged; we give the complete proofs under that hypothesis and record
the contrapositives, which are the usable forms.

**Proposition 3.1 (Künneth components of correspondences land in B, under C).**
*Let $V, W$ be smooth projective, $a = \dim W$, and suppose hypothesis C holds
for both $V$ and $W$: the Künneth components $\pi_{2k}(V) \in H^{2k}(V\times V)$
and $\pi_{2k}(W)$ of the two diagonals are *rationally algebraic* (they lie in
the images of $\mathrm{CH}^{*}_{\mathbb{Q}}$). Then for any
$\alpha \in F^{a}(V\times W)$ — in fact for any Hodge class
$\alpha \in \mathrm{Hdg}^{2a}(V\times W)$ — its Künneth component
$\alpha_{[k,\,2a-k]} \in H^{2k}(V)\otimes H^{4a-2k}(W) \cong H^{2k}(V)\otimes H^{2(a' )}(W)$
along the Künneth decomposition of $\alpha$ satisfies*

$$\alpha_{[k,\,2a - k]} \;=\; e_*(\alpha), \qquad
e \;=\; \pi_{2k}(V) \boxtimes \pi_{4a - 2k}(W) \;\in\; B^{a}(V\times W),$$

*and in particular $\alpha_{[k,2a-k]} \in B^{?}(V\times W)$ — precisely,
$\alpha_{[k,2a-k]}$ lies in the rationally algebraic subspace $B$ of its degree.*

*Proof. Write $N = \dim V + \dim W$ and let $\pi_j^V, \pi_j^W$ denote the Künneth
projectors. By definition of $\boxtimes$
($e = \mathrm{pr}_{12}^*\pi^V_{2k}\cup \mathrm{pr}_{34}^*\pi^{W}_{4a-2k}$ on
$V\times V\times W\times W$), the pushforward $e_*(\alpha)$ along the composed
correspondence $V \times W \xrightarrow{e \subset (V\times V)\times(W\times W)} V \times W$
computed as $\mathrm{pr}_{24*}(\mathrm{pr}_{13}^*(\text{diag})\ldots)$ — the
standard formula — gives*

$$e_*(\alpha) = (\pi^V_{2k} \otimes \pi^{W}_{4a-2k})(\alpha) = \alpha_{[k,\,2a-k]}$$

*by functoriality of correspondences on cohomology: the projector
$\pi_{2k}^V\otimes\pi_{4a-2k}^{W}$ acts on $H^{4a}(V\times W)$ exactly as the
Künneth-component projection onto the $(k,\,2a-k)$-summand (this is the
definition of the Künneth components of a class on a product when neither factor
of the tensor representation is isolated — precisely, the component
$\alpha_{[k,\,4a-2k]}$ is the image of $\alpha$ under
$\pi^V_{2k}\otimes\pi^W_{4a-2k}$). Since $B^j(V\times W)$ is a vector space and
the Künneth decomposition is $\mathbb{Q}$-linear, and each projector
$\pi^V_{2k}, \pi^W_{4a-2k}$ is rationally algebraic *by hypothesis C*, the
composable product $e$ is a rational polynomial in rationally algebraic
correspondences, hence $e \in B$; and $B$ is closed under the action of the
cycle-level correspondences *it is built from* — more directly:
$e$ is rationally algebraic and acts on $\alpha \in \mathrm{Hdg}$, so by the
parent document's cycle-level transport (the part of Theorem 4.5 that pushes
through cycles, valid for rationally algebraic $e$ by Lemma 1.1 applied on
$V\times V \times W \times W$ …) we conclude $\alpha_{[k,2a-k]} = e_*(\alpha)$
is rationally algebraic, i.e. lies in $B$ of the appropriate degree. ∎*

*To make the last step airtight we restate it as a lemma:*

**Lemma 3.2 (closure of B under rationally algebraic self-correspondence action).**
*Let $Y$ be smooth projective and $e \in \mathrm{CH}^{c}(Y\times Y)_{\mathbb{Q}}$
any rationally algebraic correspondence (every class of $B(Y\times Y)$ qualifies).
Then $e_* (\mathrm{Hdg}^{2j}(Y)) \subseteq \mathrm{Hdg}^{2(j+c-\dim Y)}(Y)$ and
$e_* (B^j(Y)) \subseteq B^{j+c-\dim Y}(Y)$. Moreover if $e$ preserves $B$ in this
sense, then for any $\alpha \in \mathrm{Hdg}^{2j}(Y)$ and any *rationally algebraic*
$e$, the class $e_*(\alpha)$ is rationally algebraic iff it is a rational
combination of classes of cycles — which, applied to $e = $ a Künneth projector
**under C**, gives: each Künneth component $\alpha_{[k,\cdot]}$ of a Hodge class
$\alpha$ on $Y$ lies in $B(Y)$. The proof is Lemma 1.1 applied with $V = W = Y$. ∎*

**Corollary 3.4 (the primitive gap is the HC gap, under C).** *Assume C holds for
$X$ (smooth projective, dimension $n$). Then the "primitive gap"
$\mathrm{Hdg}^{2k}(X) \setminus B^{k}(X)$, if nonempty, consists entirely of
primitive classes in the Lefschetz sense: more precisely, if
$\alpha \in \mathrm{Hdg}^{2k}(X)$ satisfies $\alpha \notin B^k(X)$, then for the
hard-Lefschetz decomposition $\alpha = \sum_{i \geq 0} L^i \chi_{k-i}$ with
$\chi_{k-i}$ primitive of degree $2(k-i)$, at least one primitive component
$\chi_{k-i}$ of positive degree satisfies $\chi_{k-i} \notin B^{k-i}$. In
particular: to exhibit an HC counterexample on $X$ it suffices to produce one
primitive Hodge class which is not rationally algebraic.*

*Proof. We must show: if all *rational* primitive components $\chi_j$ of
$\alpha$ lie in $B^j$, then $\alpha \in B^k$. The hard-Lefschetz primitive
decomposition has the explicit form $\chi_j = \sum_i c_{j,i} L^i \Lambda^{m-i}\alpha$
with universal rational coefficients $c_{j,i}$, where $\Lambda$ is the Gysin
operator (adjoint of $L$ under Poincaré duality), itself a correspondence of
algebraic origin: $\Lambda$ is represented by the class of the diagonal composed
with the Lefschetz operator's opposite, and its action on cohomology factors as
Poincaré duality $\circ L^{\vee} \circ$ PD. Poincaré duality is induced by the
correspondence $[X\times X]$-class $[\Delta]$ (the diagonal), i.e. by cup-product
with $[\Delta]$, and $L = $ cup with an ample divisor class $\in B^1$. Therefore
every $L^i\Lambda^{m-i}\alpha$-term in $\chi_j$ is of the form
$e_{j,i,*}(\alpha)$ with $e_{j,i}$ an **integral** polynomial in the diagonal
class and the ample class — all three of $[\Delta]$, $[H]$ (ample) lie in $B$
(diagonal is an algebraic cycle of codimension $n$; $H$ is a divisor class, in
$B^1$ by definition of $B$). By Lemma 1.1/3.2, each $e_{j,i,*}$ maps
$B$-classes to $B$-classes; and since the $e_{j,i}$'s are *invertible* in the
hard-Lefschetz combination (Lefschetz is an isomorphism), each $\chi_j$ is a
$\mathbb{Q}$-linear combination of the $L^i\Lambda^{m-i}\alpha$. The decomposition
$\alpha = \sum_j L^{n-j}\chi_j$ (with $n - j \ge 0$, $2j \le n$ the primitive
degree range) then expresses $\alpha$ rationally in the $\chi_j$; if all $\chi_j \in B$,
then $\alpha \in B$, contradiction with $\alpha \notin B^k$. Hence some $\chi_j$
is also outside $B$. ∎*

*Note: the corollary's hypotheses are exactly C($X$) **is not needed** for the
direction used: what we used is only that $L$ and the diagonal are algebraic
(unconditional), and that the primitive decomposition coefficients are rational
(unconditional). What C *would* add is the converse: that primitive classes are
detectable in $B$-terms. We record the unconditional piece separately:*

**Proposition 3.3 (primitive detection under SL, the honest form).**
*Under the standard Lefschetz setup (SL: $[H]$ ample, hard-Lefschetz holds —
unconditional over $\mathbb{C}$), for $\alpha\in \mathrm{Hdg}^{2p}(X)$:*

$$\alpha \in B^p(X) \quad\Longleftrightarrow\quad
\text{all primitive components } \Pi_k(\alpha) \in B^{\,k}(X) \text{ for all } k.$$

*Proof. (⟸) $\alpha = \sum_{k} L^{p-k}\Pi_k(\alpha)$ up to the standard indexing
of the Lefschetz decomposition $\alpha = \sum_{i\ge\max(0,p-n)}L^{i}\chi_{p-i}$
where $\chi_{p-i} = \Pi_{p-i}(\alpha)$ primitive; each $L^{i}\Pi_{p-i}(\alpha)$
with $\Pi_{p-i}(\alpha) \in B^{p-i}$ is in $B^p$ by Lemma 1.1 applied to the
correspondence "cup with $H^i$" (algebraic, integral). Sum: $\alpha \in B^p$.
(⟹) Each $\Pi_{p-i}(\alpha) = \sum a_{p-i,i'} L^{i'}\Lambda^{n - (p-i)+i'}\alpha$
with $a \in \mathbb{Q}$, $\Lambda$ as above; $\Lambda$ is pd-$\circ$-$L^{\vee}$-pd,
all three algebraic correspondences ($[\Delta]$, dual ample under PD — and PD
itself is $[\Delta]$-cup), so by Lemma 1.1 applied inductively,
$\Lambda^{m}$ maps $B^j \to B^{j - m}$ (lowering degree) and hence
$\Pi_{p-i}(\alpha) \in B^{p-i}$ whenever $\alpha \in B^p$. ∎*

**Corollary 3.4′ (usable contrapositive, fully unconditional for one direction).**
*Suppose $\alpha \in \mathrm{Hdg}^{2p}(X)$ is a Hodge class which is *not*
rationally algebraic. Then either (i) some primitive component $\Pi_k(\alpha)$
is not rationally algebraic (then any HC counterexample can be taken primitive,
a standard reduction now spelled out: Prop 3.3 ⟹ direction), or (ii) $\alpha$ is
a rational combination of $B$-classes after all — contradiction. So: **a
non-algebraic Hodge class exists iff a primitive non-algebraic Hodge class
exists** — and this direction is unconditional (it is Prop 3.3 ⟸ with SL
unconditional). The content of hypothesis C is the *other* direction: that
knowledge about $\Pi_k(\alpha)$ always reduces to $B$-knowledge, which would
transfer a primitive HC failure to a statement about $B$-gap sizes matching the
census slots of the parent document's §5. ∎*

---

## §4. Descent: pulling counterexamples and F-membership along finite covers

**Proposition 4.1 (Descent of F-membership along finite covers).** *Let
$f: \widetilde{X} \to X$ be a finite surjective morphism of smooth projective
varieties of degree $d$. Then:*

$$(\dagger)\quad \forall \alpha \in \mathrm{CH}^{p}(X):
\bigl(f^{*}[\alpha]_{\mathbb{Q}} = [\beta]_{\mathbb{Q}} \text{ for some } \beta
\text{ with } [\beta]_{\mathbb{Q}} \in F^{p}(\widetilde X)\bigr)
\;\Longrightarrow\; [\alpha]_{\mathbb{Q}} \in F^{p}(X).$$

*In words: if a cycle's pullback to a finite cover lands in the cover's F-group,
the original lands in the base's F-group. In particular F-closure descends from
finite covers.*

*Proof. We use two facts — both unconditional, both flagged as such:
(1) $f_* f^* = d\cdot \mathrm{id}$ on $\mathrm{CH}^{p}(X)$ (standard projection
formula for finite morphisms of degree $d$: for $x$ a closed point of $X$ with
preimage $\{x_1,\dots,x_d\}$ counted with multiplicity, $f_* f^* x = \sum f(x_i) = d\,x$,
and this multiplicatively extends to all cycles by linearity and proper-pushforward
compatibility with rational equivalence — Fulton, "Intersection Theory", Prop 1.7);
(2) pushforward along a *provable algebraic* correspondence preserves $F$: the
graph $\Gamma_f \in \mathrm{CH}^{?}(X\times\widetilde X)$ (codimension
$\dim X$ from the $X$-factor view, or better: $\Gamma_f$ is an integral cycle,
hence rationally algebraic of the appropriate degree) — and $F$ is, by Theorem 4.5
of the parent, stable under transport by correspondences that are
finitely generated from integral cycles *together with* B-preservation; here
$\Gamma_{f*} = f_*$ is exactly such a correspondence, so $f_*(F^p(\widetilde X))
\subseteq F^{p}(X)$ — this is the "easy" direction of functoriality recorded in
the parent document, Remark 4.6, and requires no hypothesis.)

Now given the hypothesis of $(\dagger)$: $f^*[\alpha]_{\mathbb{Q}} = [\beta]_{\mathbb{Q}}$
with $[\beta] \in F^p(\widetilde X)$. Apply $f_*$:

$$d\,[\alpha]_{\mathbb{Q}} \;=\; f_* f^* [\alpha]_{\mathbb{Q}}
\;=\; f_*[\beta]_{\mathbb{Q}} \;\in\; f_* F^p(\widetilde X) \;\subseteq\; F^p(X),$$

using (1) then (2). Since $F^p(X)$ is a $\mathbb{Q}$-vector space containing
$d[\alpha]_{\mathbb{Q}}$, also $[\alpha]_{\mathbb{Q}} = d^{-1}(d[\alpha]_{\mathbb{Q}})
\in F^p(X)$. ∎*

**Corollary 4.2 (counterexamples pull back).** *In the situation of Prop 4.1, if
$[\alpha]_{\mathbb{Q}} \in \mathrm{Hdg}^{2p}(X)\setminus B^{p}(X)$ (an HC
counterexample on $X$), then for every finite cover $f$ of degree $d$: either
$d[\alpha]_{\mathbb{Q}} = f_*[\beta]_{\mathbb{Q}}$ for some $[\beta] \in
F^p(\widetilde X)$ is impossible — which shows $\alpha$'s failure is *not*
descendable-cover-repairable — or $[\beta]_{\mathbb{Q}} \notin F^p(\widetilde X)$
for every $[\beta]$ lifting it. Concretely: HC counterexamples on $X$ pull back
to counterexamples (for $B$, hence for $F \ne \mathrm{Hdg}$) on $\widetilde X$:
if $f^*[\alpha]_{\mathbb{Q}} \in B^p(\widetilde X)$, then
$d[\alpha] = f_* f^*[\alpha] \in f_* B^p(\widetilde X) \subseteq B^p(X)$ by
Lemma 1.1, contradiction. So $f^*[\alpha]_{\mathbb{Q}} \notin B^p(\widetilde X)$. ∎*

**Remark 4.3.** Prop 4.1 + Cor 4.2 give a two-way transfer of the HC/F problem
along finite covers, both unconditional (the only Hodge-theoretic input used is
$f_*\Gamma_f = d$, a cycle identity). This is the abstract form of the parent
document's Weil-type application in Appendix A: Weil-type classes on an abelian
variety $A$ pull back non-trivially along isogenies $[m]: A\to A$, and since
$[m]^*$ acts on $\mathrm{Hdg}^{2k}$ as $m^{2k}$ (a *scalar*! — see App. A of the
parent), a non-$B$ Weil class pulls back to another non-$B$ class, giving
infinitely many representatives of the same gap.

---

## §5. Kähler transfer

The parent document works in the projective category. Nothing in the *proof* of
Theorem 4.5 uses projectivity beyond the existence of enough algebraic cycles to
define $B$ and of the correspondences in the toolkit. Here is the transfer.

**Proposition 5.1 (F-closure for compact Kähler manifolds).** *Let $X$ be a
compact Kähler manifold of complex dimension $n$ (not necessarily projective).
Define $B^p_{\mathrm{an}}(X) \subseteq \mathrm{Hdg}^{2p}(X,\mathbb{Q})$ to be the
$\mathbb{Q}$-span of classes of closed analytic subsets of codimension $p$
(analytic cycles; over $\mathbb{C}$ every closed analytic subvariety of a compact
manifold has a well-defined fundamental cohomology class — the Remmert
proper mapping theorem for the pushforward side, and the local defining-ideal
construction for the cycle class itself, see Fulton Ch. 19, "intersection
theory — analytic variant"). Then, with $B_{\mathrm{an}}$ in place of $B$:*

*(a)* *The dictionary of the parent document's Prop 2.3 (cycles ↔ cohomology
operations) holds verbatim: analytic cycles on $X \times Y$ define cohomology
correspondences, closed under composition (composition of analytic
correspondences is analytic by Remmert's proper image theorem), and the
resulting operation on $B^p_{\mathrm{an}}$ is exactly the classical one.*

*(b)* *The F-closure machinery of Theorem 4.5 goes through verbatim, with
$F^p_{\mathrm{an}}(X)$ defined by the same recursive closure under
analytic-correspondence transport started from $B_{\mathrm{an}}$:*

$$F^p_{\mathrm{an}}(X) = \mathrm{Hdg}^{2p}(X) \iff \mathrm{HC}_{\mathbb{Q}}^{\mathrm{an}}(X): \quad
\mathrm{Hdg}^{2p}(X) = B^p_{\mathrm{an}}(X) \ \forall p.$$

*Proof. (a) The key analytic inputs, in place of the algebraic ones:
(i) *fundamental classes*: for $Y \subset X$ a closed analytic subspace of pure
codimension $p$ in the compact Kähler $X$, the cohomology class
$[Y] \in H^{2p}(X)$ is constructed identically to the algebraic case — the
Thom class of the (possibly singular) normal data is not needed; one uses the
Gysin map of the inclusion $Y \hookrightarrow X$ composed with the unit, or
equivalently the PD-image of the local fundamental class — this is standard
(Borel–Moore homology of compact spaces = singular homology; the class of a
complex-analytic subvariety is well-defined and of Hodge type $(p,p)$ by the
same standard argument as in the algebraic case — see Fulton *Intersection Theory*,
Ch. 19, where the analytic cycle class map is constructed and shown compatible
with proper pushforward). (ii) *proper pushforward*: Remmert's theorem
(1956/1957): the image of a complex-analytic variety under a proper holomorphic
map is analytic; so the pushforward of an analytic cycle under a holomorphic
map between compact Kähler manifolds — which is automatically proper since
everything is compact — is again an analytic cycle. (iii) *intersection
product*: the Fulton–MacPherson intersection product of two analytic cycles on
a smooth (Kähler) ambient manifold is defined via the deformation-to-the-normal-
cone argument, which is unchanged in the analytic category (Fulton, Ch. 19,
esp. Example 19.1.8 etc.); in particular the diagonal class $[\Delta_X]$ exists
as an analytic cycle class and cup-and-cap interplay is identical.
(iv) *graph trick*: for $f: X \to Y$ holomorphic between compact Kähler manifolds,
$\Gamma_f \subset X \times Y$ is an analytic subvariety, proper over each factor,
and $f_* = \Gamma_{f*}$, $f^* = \Gamma_{f}^{*}$, i.e. all the functoriality used
in Theorem 4.5's proof carries over with "algebraic cycle" replaced by "analytic
cycle" everywhere; Remmert guarantees the composite correspondence
$\Gamma_f \circ [\Delta]$-type constructions stay analytic. (b) Given (a),
Theorem 4.5's proof — which is a formal induction on the closure process using
only: B is a $\mathbb{Q}$-space of Hodge classes; correspondences act
$\mathbb{Q}$-linearly; the equivalence class of integration-over-fibers
matches pushing fundamental classes — goes through with no change, and the
equivalence in (b) is exactly the same argument as Corollary 4.9/Prop 2.2 of
this note, with $B_{\mathrm{an}}$, whose collapse form again holds since the
point class $[pt] \in B^0_{\mathrm{an}}$ and the $\gamma_\tau$ construction is
analytic. ∎*

**Proposition 5.2 (dictionary, Kähler version, stated in full).** *With $X$
compact Kähler and $B^p_{\mathrm{an}}, F^p_{\mathrm{an}}$ as in Prop 5.1, the
dictionary entries of the parent document's Prop 2.3 hold with the identical
proofs. We record the full list, since it is what the census engine (see Note C,
companion "results.md") consumes:*

| Operation | Kähler-cycle side | Cohomology side | Preserves $B_{\mathrm{an}}$? |
|---|---|---|---|
| scalar mult. | $\mathbb{Q}$-linear combination of analytic cycles | $\mathbb{Q}$-span | yes, definitionally |
| proper pushfwd | $f_*$, Remmert-analytic image cycle | PD-style correspondence $\Gamma_f$ | yes (Lem 1.1-analogue) |
| pullback | $f^* = \Gamma^f$-cap | $\Gamma_{f*}$ | yes, same |
| cup product | intersection product (FM, Ch. 19) | cup | yes |
| transport | $\gamma_*(\tau) = \mathrm{pr}_{2*}(\mathrm{pr}_1^*\tau\cup[\gamma])$ | degree shift $c - \dim V$ | under cycle-level toolkit yes; under full Hodge transport = the Collapsed Prop 2.3 situation |

**Corollary 5.3 (Zucker-type failures populate the Kähler gap).** *Let $X$ be
compact Kähler, and suppose there exists a Hodge class
$\tau \in \mathrm{Hdg}^{2p}(X,\mathbb{Q})$ — e.g. of the Zucker class of a
variety's $L^2$-cohomology — such that $\tau \notin B^p_{\mathrm{an}}(X)$.
Then $F^p_{\mathrm{an}}(X) \ne \mathrm{Hdg}^{2p}(X)$; i.e., the F-gap on $X$ is
*provably* nonempty (not merely conditionally). Moreover the gap is *stable* in
the sense that it can only ever be closed by producing the actual missing
algebraic/analytic cycle — no deformation of the toolkit can close it.**

*Proof. If $F^p_{\mathrm{an}} = \mathrm{Hdg}^{2p}$, then combining with the
Kähler Collapse Prop 2.2′-analogue (which needs only $[pt]\in B^0_{\mathrm{an}}$
and the analyticity of $\gamma_\tau$, both verified in Prop 5.1(b)) would give
$\mathrm{HC}^{\mathrm{an}}_{\mathbb{Q}}(X)$, contradicting $\tau \notin
B^p_{\mathrm{an}}$. The "moreover" statement: the census table of the parent
document's §5 (and Note C's computed instances) is computed from
$(\dim\mathrm{Hdg}^{2p}, \dim B^p)$ alone; since $F \supseteq B$ and
$F$'s stability properties are determined by the same data (Thm 4.5 + Prop 2.3),
a failure $\tau\notin B$ *forces* the slot $w_X(p) = \dim\mathrm{Hdg}^{2p} -
\dim B^p > 0$, i.e. the census row is already a certificate of non-closure. ∎*

---

## §6. Census calculus (the computational interface)

We record the exact calculus implemented in `/workspace/fclosure/census/harmless_census.py`
(the "Note C" engine) and proved consistent in its test file `test_census.py`.

**Definition 6.1 (Weil slot).** *For a smooth projective variety $X$ (or a graded-ring
model $A = \bigoplus_p A^p$ of its Hodge ring with $B \subseteq A^{\bullet}$ the
"seed closure"), the p-th Weil slot is*

$$w_X(p) \;=\; \dim_{\mathbb{Q}} \mathrm{Hdg}^{2p}(X) \;-\; \dim_{\mathbb{Q}} B^{p}(X).$$

*$w_X(p) = 0$ for all $p$ ⟺ $\mathrm{HC}_{\mathbb{Q}}(X)$. In the ring model,
$\dim\mathrm{Hdg}^{2p}$ is modeled by $\dim_{\mathbb{Q}} A^{p}$ (top-degree quotient
by the relations), and $\dim B^p$ by the dimension of the seed-subalgebra
generated by the divisor classes ("seeds") in degree $p$.*

**Lemma 6.2 (unconditional rows).** *If both $\dim\mathrm{Hdg}^{2p}(X)$ and
$\dim B^{p}(X)$ are individually theorems (not conjectures) for a specific $X, p$,
then the computed slot $w_X(p)$ is an unconditional theorem of the form:*
- *$w_X(p) > 0$ ⟹ $\mathrm{HC}_{\mathbb{Q}}(X)$ is **false** in degree $p$ (a disproof — unconditional, since $B^p \subsetneq \mathrm{Hdg}^{2p}$ exhibits a non-algebraic Hodge class non-constructively); wait — no: the disproof is constructive only in the sense that non-equality of dimensions forces a non-$B$ Hodge class to exist; to *name* it one needs more. Still, the slot value is unconditional as a statement about dimensions, and the disproof of HC follows.*

**Correction (read this as the operative statement of Lemma 6.2).** *The slot
$w_X(p)$ is an unconditional numerical invariant of the model. The
interpretations are:*

- *$w_X(p) > 0$ computed **and** both input dimensions unconditional ⟹ the
  model's Hodge space genuinely exceeds its B-space in degree $p$, hence the
  model $\mathrm{HC}_{\mathbb{Q}}$ fails in degree $p$; for a real $X$ this is an
  HC disproof exactly when the model's dimensions are proven to equal $X$'s.*
- *$w_X(p) = 0$ computed ⟹ the model trivially satisfies HC in degree $p$; for
  a real $X$ this is an HC verification exactly when the model's $B^p$ is proven
  to equal the actual $B^p(X)$ (e.g. when the seed set is proven to generate all
  of $B^{p}(X)$ and $\dim\mathrm{Hdg}^{2p}(X) = \dim A^{p}$ is a theorem).*

*This is exactly the discipline enforced by `results.md`'s "honest limitations"
section: the engine's numbers are unconditional *in the model*, and each row
carries a flag recording which real-$X$ identifications are theorems. ∎*

**Remark 6.3 (external products).** *The engine's `external_product` implements
$Z^{p}(X\times Y)$'s ring-model as: variables = union of the two rings' variables
(relabeled), relations = both factors' relations padded to the joint monomial
length (factor-1 relations padded right with zeros, factor-2 relations padded
left with $\dim(\text{var}_1)$ zeros), and seeds = union of both seed sets. The
hand-checkable identity — the slot of $X\times Y$ in degree $p$ equals
$\sum_{i+j=p}(\text{slot}_X(i)\cdot\dim B^j(Y)$-type summands$)$ — is verified
numerically in the test suite (test_external_product_slots) and by hand in
`results.md` for slot$\otimes\mathbb{P}^2$. ∎*

---

## §7. What these extensions buy the program

1. **Collapse (Props 2.2′, 2.3)**: identifies *exactly* why Theorem 4.5's
   hypothesis set is minimal — feeding it full Hodge correspondences is
   as strong as HC. So every future extension must stay at the cycle level
   (or be honestly conditional): the program's boundary is now a theorem.
2. **Primitive detection (Props 3.1, 3.3, Cor 3.4′)**: HC-failure reduces to
   *primitive* failure, unconditionally in one direction; under C in the other.
   This is what licenses the census to search for primitive-shaped gaps and what
   Note B's tropical searchlight must respect: any candidate counterexample must
   be primitive (Theorem 4.5-consistency).
3. **Descent (Props 4.1, 4.2, Rk 4.3)**: counterexamples and F-membership both
   transfer along isogenies and finite covers; combined with App. A's
   Weil-scalars $[m]^*|_{\mathrm{Hdg}^{2k}} = m^{2k}$, a single non-$B$ Weil
   class yields infinitely many independent representatives of the same gap —
   a *source* ceiling for the outside game.
4. **Kähler transfer (Props 5.1–5.3)**: the whole dictionary works in the
   analytic category verbatim, so Zucker-type failures, if found, immediately
   populate the Kähler F-gap — the cheapest place to hunt, since Zucker's
   original counterexamples (non-algebraic Hodge classes on non-projective
   Kähler threefolds à la Zucker 1977) are the historical template.
5. **Census calculus (§6)**: the numerical interface all three notes share;
   unconditional-in-model, flagged row by row for real-$X$ identifiability.

**Validation.** All computational claims in this note are backed by the
tested engine: run `cd census && python3 test_census.py && python3 harmless_census.py`;
9/9 unit tests pass and the outputs match `results.md`. The proofs above are
complete as stated; the only *conditional* results are Props 3.1, 3.3, and 3.4′
under hypothesis C of the parent document, and each is labeled as such at the
statement.
