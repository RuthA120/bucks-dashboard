import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import { useFetch, Spinner, ErrorMsg, pct } from '../App'
import './ShotQuality.css'

const MIL_COLOR = '#EEE220'
const CHA_COLOR = '#7eb8c9'

function buildChartData(byQuarter) {
  if (!byQuarter?.length) return []
  const quarters = [...new Set(byQuarter.map(r => r.period))].sort()
  return quarters.map(q => {
    const mil = byQuarter.find(r => r.period === q && r.team === 'MIL')
    const cha = byQuarter.find(r => r.period === q && r.team === 'CHA')
    return {
      quarter: 'Q' + q,
      mil_fg:  mil?.fg_pct  != null ? +(mil.fg_pct  * 100).toFixed(1) : null,
      cha_fg:  cha?.fg_pct  != null ? +(cha.fg_pct  * 100).toFixed(1) : null,
      mil_qsq: mil?.avg_qsq != null ? +mil.avg_qsq : null,
      cha_qsq: cha?.avg_qsq != null ? +cha.avg_qsq : null,
      mil_qsp: mil?.avg_qsp != null ? +mil.avg_qsp : null,
      cha_qsp: cha?.avg_qsp != null ? +cha.avg_qsp : null,
    }
  })
}

const TOOLTIP_STYLE = {
  backgroundColor: '#1e1e28',
  border: '1px solid rgba(255,255,255,0.12)',
  borderRadius: '8px',
  color: '#f0f0f0',
  fontSize: '0.88rem',
}

function MetricChart({ data, milKey, chaKey, title, unit, domain }) {
  return (
    <div className="sq-chart-card">
      <div className="sq-chart-title">{title}</div>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data} margin={{ top: 8, right: 16, left: -8, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis
            dataKey="quarter"
            tick={{ fill: '#64647a', fontSize: 13, fontFamily: 'Barlow Condensed, sans-serif' }}
            axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
            tickLine={false}
          />
          <YAxis
            domain={domain || ['auto', 'auto']}
            tick={{ fill: '#64647a', fontSize: 12, fontFamily: 'Barlow Condensed, sans-serif' }}
            axisLine={false}
            tickLine={false}
            tickFormatter={v => unit === '%' ? v + '%' : v}
          />
          <Tooltip
            contentStyle={TOOLTIP_STYLE}
            formatter={(val, name) => [
              unit === '%' ? val + '%' : val,
              name === milKey ? 'MIL' : 'CHA'
            ]}
            labelStyle={{ color: '#9898a8', marginBottom: '4px' }}
            cursor={{ stroke: 'rgba(255,255,255,0.1)' }}
          />
          <Legend
            formatter={val => val === milKey ? 'MIL' : 'CHA'}
            wrapperStyle={{ fontSize: '0.82rem', color: '#9898a8', paddingTop: '8px' }}
          />
          <Line
            type="monotone"
            dataKey={milKey}
            stroke={MIL_COLOR}
            strokeWidth={2.5}
            dot={{ r: 4, fill: MIL_COLOR, strokeWidth: 0 }}
            activeDot={{ r: 6 }}
            connectNulls
          />
          <Line
            type="monotone"
            dataKey={chaKey}
            stroke={CHA_COLOR}
            strokeWidth={2.5}
            dot={{ r: 4, fill: CHA_COLOR, strokeWidth: 0 }}
            activeDot={{ r: 6 }}
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

function OverallQuality({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)'}}>No data</p>
  const mil = data.find(r => r.team === 'MIL')
  const cha = data.find(r => r.team === 'CHA')
  return (
    <div className="two-col" style={{marginBottom:'2rem'}}>
      {[{team:'MIL',row:mil,color:MIL_COLOR},{team:'CHA',row:cha,color:CHA_COLOR}].map(({team,row,color}) => (
        <div key={team} className="card">
          <div className="sq-team-heading" style={{color}}>{team === 'MIL' ? 'MILWAUKEE' : 'CHARLOTTE'}</div>
          {[
            { label: 'FG%',     val: pct(row?.fg_pct)    },
            { label: 'Avg qSQ', val: row?.avg_qsq ?? '—' },
            { label: 'Avg qSP', val: row?.avg_qsp ?? '—' },
          ].map(m => (
            <div key={m.label} className="quality-row">
              <span className="quality-metric">{m.label}</span>
              <span className="quality-val" style={{color}}>{m.val}</span>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

export default function ShotQuality() {
  const overall   = useFetch('/shot-quality/overall')
  const byQuarter = useFetch('/shot-quality/by-quarter')

  const loading = overall.loading || byQuarter.loading
  const error   = overall.error   || byQuarter.error

  if (loading) return <Spinner />
  if (error)   return <ErrorMsg msg={error} />

  const chartData = buildChartData(byQuarter.data)

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Shot Quality</h2>
        <p className="section-sub">Shot selection and probability analysis</p>
      </div>

      <div className="sq-glossary">
        <div>
          <p className="sq-glossary-term">qSQ (Shot Quality)</p>
          <p className="sq-glossary-def">Expected FG% based on shot location and context. Higher = better shot selection.</p>
        </div>
        <div>
          <p className="sq-glossary-term">qSP (Shot Probability)</p>
          <p className="sq-glossary-def">Probability the shot attempt results in points. Accounts for shot difficulty and defender proximity.</p>
        </div>
      </div>

      <p className="sub-heading">Overall Shot Quality</p>
      <OverallQuality data={overall.data} />

      <hr className="divider" />

      <p className="sub-heading">Quarter-by-Quarter Trends</p>
      <div className="sq-charts-grid">
        <MetricChart
          data={chartData}
          milKey="mil_fg"
          chaKey="cha_fg"
          title="FG% by Quarter"
          unit="%"
          domain={[0, 100]}
        />
        <MetricChart
          data={chartData}
          milKey="mil_qsq"
          chaKey="cha_qsq"
          title="Avg qSQ by Quarter"
        />
        <MetricChart
          data={chartData}
          milKey="mil_qsp"
          chaKey="cha_qsp"
          title="Avg qSP by Quarter"
        />
      </div>

    </div>
  )
}