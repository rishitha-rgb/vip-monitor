# EcoVestors Design Guidelines

## Design Philosophy
**Hybrid Approach**: Material Design foundation + B2B platform patterns (Stripe clarity, Linear efficiency, Notion organization). Balances enterprise functionality with environmental storytelling.

**Core Principles**:
- Trust Through Transparency (clear hierarchy, visible states, security indicators)
- Environmental Impact First (visualizations front-and-center)
- Role-Specific Efficiency (distinct Industry vs Artisan experiences)
- Progressive Disclosure (complex features explained simply)

## Typography

**Fonts**:
- **Inter** (Google Fonts): UI, body, data displays
- **Outfit** (Google Fonts): Marketing, heroes, headlines

**Scale**:
- Hero: Outfit, 48-72px desktop / 32-40px mobile, weight 700
- Section Headers: Outfit, 32-48px / 24-32px mobile, weight 600
- Dashboard Titles: Inter, 24-32px, weight 600
- Card Headers: Inter, 18-20px, weight 600
- Body: Inter, 16px, weight 400, line-height 1.6
- Meta/Small: Inter, 14px, weight 400-500
- Buttons: Inter, 14-16px, weight 500, uppercase tracking

## Layout & Spacing

**Spacing**: Use Tailwind units consistently: 2, 4, 6, 8, 12, 16 (p-4, m-8, gap-6, space-y-12)

**Grid**:
- Containers: max-w-7xl (dashboards), full-width (landing)
- Dashboard: 12-column (sidebar col-span-3 + main col-span-9)
- Cards: grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
- Forms: Single column max-w-2xl (simple), two-column (complex profiles)

**Vertical Rhythm**:
- Landing sections: py-16 to py-24
- Dashboard sections: py-8 to py-12
- Cards: p-6
- Forms: space-y-6

**Breakpoints**: sm:640px, md:768px, lg:1024px, xl:1280px, 2xl:1536px

## Components

### Navigation
**Top Nav**: Fixed h-16, logo left, nav center, user menu right. Role badge (Industry/Artisan) next to avatar. Sticky with shadow on scroll.

**Sidebar**: Fixed left w-64, icon+label items, active state indicators. Collapsible on mobile. Quick stats at bottom.

### Hero Section
- Split 50/50: content left, image right
- Left: Headline + subheadline + dual CTAs + trust indicators ("500+ tons recycled")
- Right: **Required hero image** - artisan with reclaimed materials or waste transformation, professional photography
- Desktop: min-h-screen, Mobile: natural height, subtle gradient overlay

### Cards

**Material Listings** (Industries):
- Elevated with hover lift, thumbnail/icon, material badge (top-right)
- Title, quantity, quality, status, "View Details" button

**Match Results** (Artisans):
- Horizontal (desktop) / vertical (mobile)
- Circular match score (0-100%), industry info, location, distance, quantity, rating
- Primary: "Send Request" button

**Requests** (Both):
- Timeline layout with status badges
- User avatar + info, material details, status progression
- Role-based actions: Accept/Reject (industries), Track/Rate (artisans)

**Achievements**:
- Gradient background (tier-based), large badge icon
- Title, description, progress bar, unlock criteria

### Dashboards

**Industry**:
- Top: 4-column metrics (Pending Requests, Materials Listed, Revenue, Carbon Impact)
- Middle: Active Requests (60%) + Inventory (40%)
- Bottom: Transaction table with pagination
- Right: Quick actions + notifications

**Artisan**:
- Top: 4 metrics (Sent Requests, Materials Acquired, Spent, Carbon Points)
- Middle: Match recommendations (horizontal scroll)
- Main: Kanban board (Pending → In Transit → Delivered → Completed)
- Side: Leaderboard + achievements

**Shared**:
- Consistent metric cards, real-time status (pulsing dots)
- Empty states with illustrations + CTAs

### Forms

**Registration**:
- Multi-step wizard with progress (Role → Basic Info → Profile → Verification)
- Step 1: Large role cards with icons
- Steps 2-4: Single-column, grouped sections, inline validation
- Material requirements (Artisans): Dynamic tag-based input

**Request Form** (Artisans):
- Modal with backdrop blur, single-column
- Material selector (searchable dropdown), quantity (min/max), timeline picker, notes
- Auto-calculated cost preview
- Cancel (secondary) + Send Request (primary)

### Data Displays

**Matching Interface**:
- Left: Filter sidebar (type, location radius, quantity, quality)
- Main: Results grid with scores, map view toggle
- Results count + sort dropdown (Best Match, Nearest, Highest Rated)

**Transaction Tracker**:
- Stepper: Request Sent → Accepted → Escrowed → In Transit → Delivered → Confirmed
- Blockchain link per payment step, estimated dates, current step highlighted

**Leaderboard**:
- Rank (medals for top 3), avatar + name + role badge
- Carbon points with trend arrow, impact metric, achievements count
- Alternating rows, sticky header

### Gamification

**Carbon Points**:
- Circular progress to next tier, animated count-up
- Tier name/icon (Bronze/Silver/Gold/Platinum) + benefits

**Best Artisan**:
- Featured card with large profile image, story (expandable)
- Like count, comment preview, share buttons, previous winners carousel

**Impact Graphs**:
- Line (carbon over time), bar (vs community avg), donut (material types)
- Use Material Design data viz patterns

### Blockchain/Payment

**Escrow Widget**:
- Transaction state, wallet address (truncated + copy), amount (ETH + USD)
- Gas estimate, status badge, Etherscan link, release button (artisans)

### Notifications

**Toast**: Top-right slide-in, icon + title + message + timestamp, dismiss button, auto-dismiss 5s

**Banners**: Full-width, color-coded (yellow:warning, green:success, blue:info), closeable

### Support Pages

**Help**: Search bar, FAQ accordion, video grid, contact form, live chat (bottom-right)

**Privacy**: Single-column max-w-4xl, sticky TOC sidebar, section anchors, last updated date

## Images

**Hero**: **Required** - Professional photo: artisan with industrial waste materials OR split image (waste → artisan products). Conveys transformation. Placement: right 50% (desktop), edge-to-edge (mobile).

**Landing**: How-it-works steps, success stories (real products), impact before/after, community photos

**Dashboard**: User avatars, material listing photos (or placeholders)

## Interactions

**Loading**: Skeleton screens (dashboards), spinners (forms), progress bars (uploads), shimmer (images)

**Hover**: Cards (shadow-md → shadow-lg), buttons (Material Design states), links (underline), table rows (background highlight)

**Micro-interactions**: Success checkmark animation, counter animations, confetti (achievements), smooth transitions (tabs, modals)

## Responsive

**Mobile**:
- Sidebar → bottom tab bar
- Metrics stack to 1 column
- Tables → expandable card lists
- Multi-column grids → single column
- Hero stacks content over image

**Desktop**:
- Dense data layouts, multi-column comparisons
- Persistent sidebar, hover tooltips, larger visualizations

## Accessibility
- Follow Material Design accessibility standards
- WCAG AA minimum for color contrast
- Keyboard navigation for all interactive elements
- Screen reader labels on icons and graphics
- Form validation with clear error messaging
- Focus indicators on all focusable elements

---
**Token Budget**: ~1,950 tokens. All critical design rules, components, patterns, and requirements preserved for developer implementation.