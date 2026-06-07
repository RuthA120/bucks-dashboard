import { useFetch, Spinner, ErrorMsg } from '../App'
import './PickAndRoll.css'

const SCHEME_META = {
  over:   { label: 'Go Over',  color: '#2f80c8' },
  under:  { label: 'Go Under', color: '#c87a2f' },
  switch: { label: 'Switch',   color: '#7a4ac8' },
}

function CoverageCards({ row }) {
  const schemes = ['over', 'under', 'switch']
  return (
    <div className="coverage-cards-grid">
      {schemes.map(scheme => {
        const { label, color } = SCHEME_META[scheme]
        const count      = row[`${scheme}_count`]      ?? 0
        const ptsAllowed = row[`pts_allowed_${scheme}`] ?? 0
        const ptsPerPoss = row[`pts_per_${scheme}`]     ?? null
        return (
          <div key={scheme} className="coverage-card">
            <div className="coverage-card-scheme" style={{ borderColor: color, color }}>
              {label}
            </div>
            <div className="coverage-card-main">
              <span className="coverage-card-pts">{ptsPerPoss ?? '—'}</span>
              <span className="coverage-card-pts-label">pts / poss</span>
            </div>
            <div className="coverage-card-footer">
              <span>{count} possessions</span>
              <span>{ptsAllowed} pts allowed</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function CoverageSection({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)'}}>No data</p>
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {data.map((row, i) => (
        <div key={i}>
          <p className="sub-heading" style={{ marginBottom: '0.75rem' }}>{row.team} Defense</p>
          <CoverageCards row={row} />
        </div>
      ))}
    </div>
  )
}

function PnROffenseGrid({ data, team }) {
  const row = data?.find(r => r.team === team)
  if (!row) return <p style={{color:'var(--text3)'}}>No data</p>
  const colorClass = team === 'MIL' ? 'mil' : 'cha'
  const stats = [
    { label: 'Roll Actions', val: row.roll_actions },
    { label: 'Roll Pts',     val: row.roll_pts },
    { label: 'Pts/Roll',     val: row.pts_per_roll },
    { label: 'Pop Actions',  val: row.pop_actions },
    { label: 'Pop Pts',      val: row.pop_pts },
    { label: 'Pts/Pop',      val: row.pts_per_pop },
  ]
  return (
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'10px'}}>
      {stats.map(s => (
        <div key={s.label} className="pnr-stat-card">
          <div className="pnr-stat-label">{s.label}</div>
          <div className={`pnr-stat-value ${colorClass}`}>{s.val ?? '—'}</div>
        </div>
      ))}
    </div>
  )
}

export default function PickAndRoll() {
  const offense      = useFetch('/pick-and-roll/offense')
  const rollCoverage = useFetch('/pick-and-roll/defense/roll-coverage')
  const popCoverage  = useFetch('/pick-and-roll/defense/pop-coverage')

  const loading = offense.loading || rollCoverage.loading || popCoverage.loading
  const error   = offense.error   || rollCoverage.error   || popCoverage.error

  if (loading) return <Spinner />
  if (error)   return <ErrorMsg msg={error} />

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Pick &amp; Roll / Pop</h2>
        <p className="section-sub">Screen offense efficiency and defensive coverage breakdowns</p>
      </div>

      <p className="sub-heading">Offense — Roll &amp; Pop Stats</p>
      <div className="drives-glossary">
        <strong>Pick and Roll Action</strong> — involving two offensive players, one sets a screen for the primary ball handler and after setting it they roll to the basket to receive a pass and score. <br></br>
        <strong>Pick and Pop Action</strong> — similar to above definition except ball screener will move to an open area of the court to receive a pass from the ball handler and take a jump shot. <br></br>
        <strong>Roll PTS</strong> - measuring how many points were scored on roll opportunities <br></br>
        <strong>Pop PTS</strong> - measuring how many points were scored on pop opportunities <br></br>
      </div>
      <div className="two-col" style={{marginBottom:'2rem'}}>
        <div>
          <p className="pnr-team-label" style={{color:'var(--mil-accent)'}}>Milwaukee</p>
          <PnROffenseGrid data={offense.data} team="MIL" />
        </div>
        <div>
          <p className="pnr-team-label" style={{color:'var(--cha-color)'}}>Charlotte</p>
          <PnROffenseGrid data={offense.data} team="CHA" />
        </div>
      </div>

      <hr className="divider" />
      <div className="drives-glossary">
        <strong>"Over" Screen Coverage</strong> — on-ball defender goes over the top of the screen <br></br>
        <strong>"Under" Screen Coverage</strong> — on-ball defender goes under the screen <br></br>
        <strong>"Switch" Screen Coverage</strong> - defenders of the ball-handler and screener "switch" assignments after screen<br></br>
      </div>
      <p className="sub-heading">Roll Coverage — Points Allowed by Scheme</p>
      <CoverageSection data={rollCoverage.data} />

      <hr className="divider" />
      <p className="sub-heading">Pop Coverage — Points Allowed by Scheme</p>
      <CoverageSection data={popCoverage.data} />
    </div>
  )
}
