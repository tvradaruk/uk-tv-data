# UK TV data from TV Radar

Open data behind [TV Radar](https://tvradar.uk), a free UK TV guide covering 32 Freeview channels.
Free to reuse with credit (CC BY 4.0, see [Licence](#licence)).

| Dataset | What it is | Rows |
|---|---|---|
| [`freeview/freeview-channel-numbers.csv`](freeview/freeview-channel-numbers.csv) | Freeview channel numbers (LCNs), operator, HD flag | 64 channels |
| [`repeats/repeats-by-channel-2026-08-02_to_2026-09-18.csv`](repeats/repeats-by-channel-2026-08-02_to_2026-09-18.csv) | How much of each channel's output is repeats | 32 channels |
| [`repeats/repeats-by-title-2026-08-02_to_2026-09-18.csv`](repeats/repeats-by-title-2026-08-02_to_2026-09-18.csv) | How often each title aired, and on which channels | 2,246 titles |

## Freeview channel numbers

`freeview-channel-numbers.csv` is the standard UK national Freeview line-up as of October 2026.

| Column | Meaning |
|---|---|
| `lcn` | Logical Channel Number, the number you type on the remote |
| `channel` | Channel name, with any regional notes |
| `operator` | Who runs the channel |
| `hd_on_freeview` | `yes` if there is an HD version on Freeview |
| `tvradar_guide` | That channel's daily TV guide on TV Radar, where one exists |

Some numbers differ by region (for example BBC Four is 24 in Scotland) and Freeview reshuffles numbers a few times a year. The maintained version, with regional notes, is the [Freeview channel guide](https://tvradar.uk/freeview-channel-guide).

## Repeats study

These files back the study [Why are there so many repeats on TV?](https://tvradar.uk/why-are-there-so-many-repeats-on-tv), which found that **87.9% of Freeview slots were repeats** across 32 channels between 2 August and 18 September 2026 (48 days, 41,321 slots).

The headline is reproducible from `repeats-by-channel`: weight each channel's `repeat_rate_pct` by its `slots_excl_filler`.

**Definitions**

- **Repeat**: a title the same channel had already shown at least once inside the 48-day window. This is *not* the regulatory "first run vs repeat" distinction, because the listings feed does not reliably flag new episodes. It measures how often channels return to the same titles.
- **Filler**: teleshopping, closedowns, continuity and news stings. Excluded from the headline figure.

**`repeats-by-channel`** columns: `channel` (TV Radar slug), `slots_excl_filler`, `distinct_titles`, `repeat_rate_pct`, `most_shown_title`, `its_airings`.

**`repeats-by-title`** columns: `title` (lower-cased), `airings`, `channels` (how many), `channel_list` (space-separated slugs).

Pre-school channels (CBeebies, CBBC) top the table because they repeat by design. The study discusses them separately.

## Method

The schedule data comes from the daily Freeview electronic programme guide, which TV Radar collects and processes automatically for its listings. Counting is automated. The files contain only counts and public facts. They do not reproduce programme listings or synopses.

Corrections are welcome: open an issue, or use the [contact page](https://tvradar.uk/contact).

## Licence

[Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0). Reuse it, including commercially, with credit and a link:

> Source: [TV Radar](https://tvradar.uk)

## Citation

See [`CITATION.cff`](CITATION.cff), or use GitHub's "Cite this repository" button.
