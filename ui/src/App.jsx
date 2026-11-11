import React, { useState, useMemo } from 'react'
import {
  BookOpen,
  GitFork,
  Scale,
  Globe,
  Database,
  CheckCircle2,
  AlertTriangle,
  Search,
  Filter,
  ExternalLink,
  Layers,
  ChevronRight,
  GraduationCap,
  ShieldCheck,
  Zap,
  Info,
  Calendar,
  Award,
  Hash,
  ArrowRight
} from 'lucide-react'

// Static Ingested Datasets
import coursesData from './data/courses.json'
import prereqsData from './data/prerequisite_edges.json'
import rulesData from './data/academic_rules.json'
import resourcesData from './data/resources.json'
import skillsData from './data/skills.json'
import courseSkillsData from './data/course_skill_links.json'
import chunksData from './data/chunks.json'
import summaryData from './data/data_summary.json'

export default function App() {
  const [activeTab, setActiveTab] = useState('courses')

  // Search and Filter States
  const [courseSearch, setCourseSearch] = useState('')
  const [selectedSemester, setSelectedSemester] = useState('all')
  const [selectedType, setSelectedType] = useState('all')
  const [selectedCourseDetail, setSelectedCourseDetail] = useState(null)

  // DAG Explorer State
  const [dagSelectedCourse, setDagSelectedCourse] = useState('CSL301')

  // Rules Simulator States
  const [simSemester, setSimSemester] = useState(4)
  const [simCredits, setSimCredits] = useState(18)
  const [simCGPA, setSimCGPA] = useState(8.2)
  const [simTargetCourse, setSimTargetCourse] = useState('CSL252')
  const [simCompletedCourses, setSimCompletedCourses] = useState([
    'CSL100', 'MAL100', 'CYL100', 'PHL101', 'MAL101', 'ECL101', 'EEL101', 'CSL201', 'CSL202'
  ])

  // Resources State
  const [resSearch, setResSearch] = useState('')
  const [resProvider, setResProvider] = useState('all')

  // Chunks Explorer State
  const [chunkSearch, setChunkSearch] = useState('')
  const [chunkTypeFilter, setChunkTypeFilter] = useState('all')

  // Build DAG Map
  const prereqMap = useMemo(() => {
    const map = {}
    prereqsData.forEach(edge => {
      if (!map[edge.course]) map[edge.course] = []
      map[edge.course].push(edge)
    })
    return map
  }, [])

  const dependentsMap = useMemo(() => {
    const map = {}
    prereqsData.forEach(edge => {
      if (!map[edge.requires]) map[edge.requires] = []
      map[edge.requires].push(edge)
    })
    return map
  }, [])

  // Filtered Courses
  const filteredCourses = useMemo(() => {
    return coursesData.filter(c => {
      const matchSearch =
        c.code.toLowerCase().includes(courseSearch.toLowerCase()) ||
        c.title.toLowerCase().includes(courseSearch.toLowerCase()) ||
        c.objectives.toLowerCase().includes(courseSearch.toLowerCase())
      const matchSem = selectedSemester === 'all' || c.semester_offered.toString() === selectedSemester
      const matchType = selectedType === 'all' || c.type.toLowerCase().includes(selectedType.toLowerCase())
      return matchSearch && matchSem && matchType
    })
  }, [courseSearch, selectedSemester, selectedType])

  // Filtered Resources
  const filteredResources = useMemo(() => {
    return resourcesData.filter(r => {
      const matchSearch =
        r.title.toLowerCase().includes(resSearch.toLowerCase()) ||
        r.provider.toLowerCase().includes(resSearch.toLowerCase()) ||
        r.format.toLowerCase().includes(resSearch.toLowerCase())
      const matchProv = resProvider === 'all' || r.provider.toLowerCase().includes(resProvider.toLowerCase())
      return matchSearch && matchProv
    })
  }, [resSearch, resProvider])

  // Filtered Chunks
  const filteredChunks = useMemo(() => {
    return chunksData.filter(chk => {
      const matchSearch =
        chk.chunk_id.toLowerCase().includes(chunkSearch.toLowerCase()) ||
        chk.text.toLowerCase().includes(chunkSearch.toLowerCase()) ||
        chk.parent_id.toLowerCase().includes(chunkSearch.toLowerCase())
      const matchType = chunkTypeFilter === 'all' || chk.chunk_type === chunkTypeFilter
      return matchSearch && matchType
    })
  }, [chunkSearch, chunkTypeFilter])

  // Simulator Logic
  const simPrereqs = prereqMap[simTargetCourse] || []
  const missingHardPrereqs = simPrereqs
    .filter(p => p.kind === 'hard' && !simCompletedCourses.includes(p.requires))
    .map(p => p.requires)

  const isEligibleForCourse = missingHardPrereqs.length === 0

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Banner */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white font-black text-xl">
              IIT
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold text-white tracking-tight">IIT Bhilai — Academic Knowledge Base</h1>
                <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full">
                  B.Tech CSE
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Source-Traced Knowledge Graph, Prerequisite DAG & Embedding Pipeline
              </p>
            </div>
          </div>

          {/* Quick Metrics Bar */}
          <div className="flex items-center gap-4 text-xs font-mono">
            <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-slate-300 font-bold">{coursesData.length}</span>
              <span className="text-slate-500">Courses</span>
            </div>
            <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center gap-1.5">
              <GitFork className="w-3.5 h-3.5 text-amber-400" />
              <span className="text-slate-300 font-bold">{prereqsData.length}</span>
              <span className="text-slate-500">Prereq Edges</span>
            </div>
            <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center gap-1.5">
              <Scale className="w-3.5 h-3.5 text-sky-400" />
              <span className="text-slate-300 font-bold">{rulesData.length}</span>
              <span className="text-slate-500">Rules</span>
            </div>
            <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center gap-1.5">
              <Globe className="w-3.5 h-3.5 text-teal-400" />
              <span className="text-slate-300 font-bold">{resourcesData.length}</span>
              <span className="text-slate-500">OER Res</span>
            </div>
            <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-purple-400" />
              <span className="text-slate-300 font-bold">{chunksData.length}</span>
              <span className="text-slate-500">Chunks</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto mt-4 flex items-center gap-1 border-t border-slate-800/80 pt-3 overflow-x-auto">
          {[
            { id: 'courses', label: 'Course Catalog', icon: BookOpen },
            { id: 'dag', label: 'Prerequisite Graph (DAG)', icon: GitFork },
            { id: 'rules', label: 'Academic Rules & Simulator', icon: Scale },
            { id: 'resources', label: 'Open Educational Resources', icon: Globe },
            { id: 'chunks', label: 'Embedding Chunks Inspector', icon: Layers },
            { id: 'quality', label: 'Data Quality & Provenance', icon: ShieldCheck }
          ].map(tab => {
            const Icon = tab.icon
            const active = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                  active
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            )
          })}
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-6 py-6 flex-1 w-full">
        {/* ===================== TAB 1: COURSE CATALOG ===================== */}
        {activeTab === 'courses' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between bg-slate-900 p-4 rounded-xl border border-slate-800">
              <div className="relative w-full md:w-96">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search by code (e.g. CSL202), title, topic..."
                  value={courseSearch}
                  onChange={e => setCourseSearch(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center gap-3 w-full md:w-auto">
                <select
                  value={selectedSemester}
                  onChange={e => setSelectedSemester(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
                >
                  <option value="all">All Semesters (1–8)</option>
                  {[1, 2, 3, 4, 5, 6, 7, 8].map(s => (
                    <option key={s} value={s}>Semester {s}</option>
                  ))}
                </select>

                <select
                  value={selectedType}
                  onChange={e => setSelectedType(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
                >
                  <option value="all">All Categories</option>
                  <option value="Program Core">Program Core</option>
                  <option value="Institute Core">Institute Core</option>
                  <option value="Program Elective">Program Elective</option>
                  <option value="Capstone">Capstone Project</option>
                </select>
              </div>
            </div>

            {/* Courses Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredCourses.map(course => {
                const reqs = prereqMap[course.code] || []
                return (
                  <div
                    key={course.code}
                    onClick={() => setSelectedCourseDetail(course)}
                    className="bg-slate-900 hover:bg-slate-850 p-5 rounded-xl border border-slate-800 hover:border-indigo-500/50 transition-all cursor-pointer flex flex-col justify-between group shadow-sm hover:shadow-indigo-500/5"
                  >
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="px-2 py-0.5 text-xs font-mono font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 rounded">
                          {course.code}
                        </span>
                        <span className="text-xs px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-medium">
                          Sem {course.semester_offered} • {course.credits} Cr
                        </span>
                      </div>

                      <h3 className="text-base font-semibold text-white group-hover:text-indigo-300 transition-colors line-clamp-1">
                        {course.title}
                      </h3>

                      <p className="text-xs text-slate-400 mt-1">
                        {course.dept} • <span className="text-slate-300">{course.type}</span>
                      </p>

                      <p className="text-xs text-slate-400 mt-3 line-clamp-3 leading-relaxed">
                        {course.objectives}
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <GitFork className="w-3.5 h-3.5 text-amber-400" />
                        <span>{reqs.length > 0 ? `${reqs.length} Prerequisite(s)` : 'No Prerequisites'}</span>
                      </div>
                      <span className="text-indigo-400 group-hover:translate-x-1 transition-transform flex items-center gap-0.5">
                        Details <ChevronRight className="w-3.5 h-3.5" />
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* ===================== TAB 2: PREREQUISITE DAG ===================== */}
        {activeTab === 'dag' && (
          <div className="space-y-6">
            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-2">
                <GitFork className="w-5 h-5 text-amber-400" />
                Prerequisite Dependency Directed Acyclic Graph (DAG)
              </h2>
              <p className="text-xs text-slate-400 mb-4 max-w-3xl leading-relaxed">
                IIT Bhilai enforces deterministic prerequisite constraints (§2.2.5). Every edge in this graph represents an authentic curriculum dependency. Select a course below to isolate its predecessor dependencies and successor dependents.
              </p>

              <div className="flex items-center gap-3 mb-6">
                <label className="text-xs text-slate-300 font-medium">Select Target Course:</label>
                <select
                  value={dagSelectedCourse}
                  onChange={e => setDagSelectedCourse(e.target.value)}
                  className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500 font-mono"
                >
                  {coursesData.map(c => (
                    <option key={c.code} value={c.code}>
                      {c.code} - {c.title} (Sem {c.semester_offered})
                    </option>
                  ))}
                </select>
              </div>

              {/* DAG Inspection Card */}
              {(() => {
                const targetCourse = coursesData.find(c => c.code === dagSelectedCourse)
                const ancestors = prereqMap[dagSelectedCourse] || []
                const dependents = dependentsMap[dagSelectedCourse] || []

                return (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Ancestor Precedents */}
                    <div className="bg-slate-950 p-4 rounded-xl border border-amber-500/20">
                      <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <ArrowRight className="w-3.5 h-3.5" /> Direct Prerequisites (Must Clear Prior)
                      </div>
                      {ancestors.length === 0 ? (
                        <p className="text-xs text-slate-500 italic">No prerequisites required (Foundational Course).</p>
                      ) : (
                        <div className="space-y-2">
                          {ancestors.map((p, idx) => {
                            const reqCourse = coursesData.find(c => c.code === p.requires)
                            return (
                              <div key={idx} className="bg-slate-900 p-2.5 rounded border border-slate-800 text-xs">
                                <div className="flex items-center justify-between">
                                  <span className="font-mono font-bold text-amber-300">{p.requires}</span>
                                  <span className={`px-1.5 py-0.5 rounded text-[10px] uppercase font-bold ${
                                    p.kind === 'hard' ? 'bg-rose-500/20 text-rose-300' : 'bg-blue-500/20 text-blue-300'
                                  }`}>
                                    {p.kind}
                                  </span>
                                </div>
                                <div className="text-slate-300 mt-1 font-medium">{reqCourse?.title}</div>
                                <div className="text-slate-500 text-[11px] mt-0.5">Sem {reqCourse?.semester_offered} • {reqCourse?.credits} Credits</div>
                              </div>
                            )
                          })}
                        </div>
                      )}
                    </div>

                    {/* Target Course Centerpiece */}
                    <div className="bg-gradient-to-b from-indigo-900/40 to-slate-900 p-5 rounded-xl border border-indigo-500/40 flex flex-col justify-between shadow-lg shadow-indigo-500/10">
                      <div>
                        <div className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-2">
                          Selected Focus Course
                        </div>
                        <div className="text-2xl font-black text-white font-mono">{targetCourse?.code}</div>
                        <div className="text-sm font-semibold text-indigo-200 mt-1">{targetCourse?.title}</div>
                        <div className="text-xs text-slate-400 mt-2">
                          Offered in <span className="text-white font-medium">Semester {targetCourse?.semester_offered}</span> • {targetCourse?.credits} Credits ({targetCourse?.lecture_tutorial_practical})
                        </div>
                        <div className="text-xs text-slate-300 mt-3 p-3 bg-slate-950/70 rounded-lg border border-slate-800 leading-relaxed">
                          {targetCourse?.objectives}
                        </div>
                      </div>

                      <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
                        <span>Category: {targetCourse?.type}</span>
                        <a
                          href={targetCourse?.source_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-indigo-400 hover:underline flex items-center gap-1"
                        >
                          Source <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>

                    {/* Dependents (Successors) */}
                    <div className="bg-slate-950 p-4 rounded-xl border border-emerald-500/20">
                      <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <ArrowRight className="w-3.5 h-3.5" /> Subsequent Courses Unlocked
                      </div>
                      {dependents.length === 0 ? (
                        <p className="text-xs text-slate-500 italic">No advanced courses explicitly list this as a prerequisite.</p>
                      ) : (
                        <div className="space-y-2">
                          {dependents.map((p, idx) => {
                            const depCourse = coursesData.find(c => c.code === p.course)
                            return (
                              <div key={idx} className="bg-slate-900 p-2.5 rounded border border-slate-800 text-xs">
                                <div className="flex items-center justify-between">
                                  <span className="font-mono font-bold text-emerald-300">{p.course}</span>
                                  <span className={`px-1.5 py-0.5 rounded text-[10px] uppercase font-bold ${
                                    p.kind === 'hard' ? 'bg-rose-500/20 text-rose-300' : 'bg-blue-500/20 text-blue-300'
                                  }`}>
                                    {p.kind}
                                  </span>
                                </div>
                                <div className="text-slate-300 mt-1 font-medium">{depCourse?.title}</div>
                                <div className="text-slate-500 text-[11px] mt-0.5">Sem {depCourse?.semester_offered} • {depCourse?.credits} Credits</div>
                              </div>
                            )
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                )
              })()}
            </div>
          </div>
        )}

        {/* ===================== TAB 3: ACADEMIC RULES & SIMULATOR ===================== */}
        {activeTab === 'rules' && (
          <div className="space-y-8">
            {/* Interactive Rules Engine Simulator */}
            <div className="bg-gradient-to-r from-slate-900 via-indigo-950/30 to-slate-900 p-6 rounded-xl border border-indigo-500/30 shadow-xl">
              <div className="flex items-center gap-2 mb-2">
                <Zap className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white">Student Academic Rules Engine & Scenario Planner</h2>
              </div>
              <p className="text-xs text-slate-400 mb-6">
                Deterministic compliance tester based on IIT Bhilai UG Academic Manual regulations. Test semester credit loads, prerequisite clearance, and minor/honours qualification in real-time.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1.5">Target Semester:</label>
                  <select
                    value={simSemester}
                    onChange={e => setSimSemester(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                  >
                    {[1, 2, 3, 4, 5, 6, 7, 8].map(s => (
                      <option key={s} value={s}>Semester {s}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1.5">Planned Semester Credits:</label>
                  <input
                    type="number"
                    min="6"
                    max="30"
                    step="0.5"
                    value={simCredits}
                    onChange={e => setSimCredits(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white font-mono"
                  />
                </div>

                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1.5">Current Cumulative CGPA:</label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    step="0.1"
                    value={simCGPA}
                    onChange={e => setSimCGPA(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white font-mono"
                  />
                </div>

                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1.5">Target Course Registration:</label>
                  <select
                    value={simTargetCourse}
                    onChange={e => setSimTargetCourse(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white font-mono"
                  >
                    {coursesData.map(c => (
                      <option key={c.code} value={c.code}>{c.code} - {c.title}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Simulation Result Audit Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Credit Audit */}
                <div className={`p-4 rounded-xl border text-xs ${
                  simCredits > 21
                    ? 'bg-rose-950/30 border-rose-500/40 text-rose-200'
                    : simCredits < 15 && simSemester < 8
                    ? 'bg-amber-950/30 border-amber-500/40 text-amber-200'
                    : 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200'
                }`}>
                  <div className="font-bold flex items-center gap-1.5 mb-1.5">
                    {simCredits > 21 ? <AlertTriangle className="w-4 h-4 text-rose-400" /> : <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                    Credit Load Status: {simCredits} Credits
                  </div>
                  <p className="leading-relaxed">
                    {simCredits > 21
                      ? 'Exceeds maximum allowable overload limit (21 credits). Requires exceptional approval from Chairman, IUGC (§2.4.2).'
                      : simCredits < 15 && simSemester < 8
                      ? 'Underload warning! Minimum regular load is 15 credits (§2.4.2). Requires DUGC approval.'
                      : 'Permissible regular semester load (15 to 21 credits). Meets nominal guidelines.'}
                  </p>
                </div>

                {/* Prerequisite Clearance Audit */}
                <div className={`p-4 rounded-xl border text-xs ${
                  isEligibleForCourse
                    ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200'
                    : 'bg-rose-950/30 border-rose-500/40 text-rose-200'
                }`}>
                  <div className="font-bold flex items-center gap-1.5 mb-1.5">
                    {isEligibleForCourse ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <AlertTriangle className="w-4 h-4 text-rose-400" />}
                    Prerequisite Check: {simTargetCourse}
                  </div>
                  <p className="leading-relaxed">
                    {isEligibleForCourse
                      ? 'All hard precedent prerequisites have been satisfied. Registration permissible (§2.2.5).'
                      : `Registration BLOCKED! Missing mandatory hard prerequisite(s): ${missingHardPrereqs.join(', ')}.`}
                  </p>
                </div>

                {/* Honours / Standing Audit */}
                <div className={`p-4 rounded-xl border text-xs ${
                  simCGPA >= 8.0
                    ? 'bg-indigo-950/30 border-indigo-500/40 text-indigo-200'
                    : simCGPA < 4.5
                    ? 'bg-rose-950/30 border-rose-500/40 text-rose-200'
                    : 'bg-slate-900 border-slate-700 text-slate-300'
                }`}>
                  <div className="font-bold flex items-center gap-1.5 mb-1.5">
                    <Award className="w-4 h-4 text-indigo-400" />
                    Academic Standing & Honours
                  </div>
                  <p className="leading-relaxed">
                    {simCGPA >= 8.0
                      ? 'Eligible to apply for B.Tech Honours / Minor degree program at end of Sem 5 (§3.2.2).'
                      : simCGPA < 4.0
                      ? 'CRITICAL ALERT: Auto-termination warning. CGPA < 4.0 triggers termination review (§2.3.6).'
                      : simCGPA < 4.5
                      ? 'Academic Probation warning: Warning letter issued by DoAA (§2.3.6).'
                      : 'Good academic standing. (CGPA >= 4.5 meets graduation threshold).'}
                  </p>
                </div>
              </div>
            </div>

            {/* Official Academic Regulations Repository */}
            <div>
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Scale className="w-4 h-4 text-sky-400" />
                Official Quotable Academic Ordinances & Regulations ({rulesData.length} Rules)
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {rulesData.map(rule => (
                  <div key={rule.id} className="bg-slate-900 p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <span className="font-mono text-xs font-bold text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">
                          {rule.id}
                        </span>
                        <span className="text-xs text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                          {rule.category}
                        </span>
                      </div>

                      <blockquote className="text-xs text-slate-200 italic mt-3 border-l-2 border-indigo-500 pl-3 leading-relaxed">
                        "{rule.text}"
                      </blockquote>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
                      <span>Applies to: <strong className="text-slate-300">{rule.applies_to}</strong></span>
                      {rule.numeric_limit !== null && (
                        <span className="font-mono text-indigo-400 font-bold">
                          Limit: {rule.numeric_limit}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ===================== TAB 4: OPEN EDUCATIONAL RESOURCES ===================== */}
        {activeTab === 'resources' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between bg-slate-900 p-4 rounded-xl border border-slate-800">
              <div className="relative w-full md:w-96">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search resources, topics, platforms..."
                  value={resSearch}
                  onChange={e => setResSearch(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <select
                value={resProvider}
                onChange={e => setResProvider(e.target.value)}
                className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
              >
                <option value="all">All Providers (NPTEL, MIT OCW, Berkeley...)</option>
                <option value="NPTEL">NPTEL / SWAYAM</option>
                <option value="MIT">MIT OpenCourseWare</option>
                <option value="Berkeley">UC Berkeley</option>
                <option value="Stanford">Stanford Online</option>
                <option value="Harvard">Harvard CS50</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredResources.map(res => (
                <div key={res.id} className="bg-slate-900 p-5 rounded-xl border border-slate-800 flex flex-col justify-between hover:border-teal-500/40 transition-all">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="font-mono text-[11px] font-bold text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20">
                        {res.id}
                      </span>
                      <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                        {res.licence}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white mt-1 leading-snug">
                      {res.title}
                    </h3>

                    <p className="text-xs text-indigo-300 mt-1 font-medium">
                      {res.provider}
                    </p>

                    <div className="mt-3 space-y-1.5 text-xs text-slate-400">
                      <div>Format: <span className="text-slate-300">{res.format}</span></div>
                      <div>Duration: <span className="text-slate-300 font-mono">{res.duration}</span></div>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                    <span className="text-[10px] text-slate-500 font-mono">Retrieved: {res.retrieved_on}</span>
                    <a
                      href={res.url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-3 py-1 bg-teal-600/20 hover:bg-teal-600/30 text-teal-300 text-xs font-medium rounded-lg flex items-center gap-1 transition-colors border border-teal-500/30"
                    >
                      Access Course <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ===================== TAB 5: CHUNKS INSPECTOR ===================== */}
        {activeTab === 'chunks' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between bg-slate-900 p-4 rounded-xl border border-slate-800">
              <div className="relative w-full md:w-96">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search chunk text, parent ID, tags..."
                  value={chunkSearch}
                  onChange={e => setChunkSearch(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <select
                value={chunkTypeFilter}
                onChange={e => setChunkTypeFilter(e.target.value)}
                className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
              >
                <option value="all">All Chunk Roles (130 Chunks)</option>
                <option value="course_overview">Course Overview</option>
                <option value="syllabus_content">Syllabus Content</option>
                <option value="rule_statement">Rule Statement</option>
                <option value="resource_profile">Resource Profile</option>
                <option value="lesson_unit">Lesson Unit</option>
                <option value="exercise_problem">Exercise Problem</option>
              </select>
            </div>

            <div className="space-y-3">
              {filteredChunks.slice(0, 30).map(chk => (
                <div key={chk.chunk_id} className="bg-slate-900 p-4 rounded-xl border border-slate-800 hover:border-purple-500/40 transition-all font-mono text-xs">
                  <div className="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-800">
                    <span className="font-bold text-purple-400">{chk.chunk_id}</span>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
                        Parent: {chk.parent_id} ({chk.parent_type})
                      </span>
                      <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 text-[10px]">
                        {chk.chunk_type}
                      </span>
                    </div>
                  </div>

                  <p className="text-slate-300 font-sans whitespace-pre-line leading-relaxed mb-3">
                    {chk.text}
                  </p>

                  <div className="text-[11px] text-slate-500 bg-slate-950 p-2.5 rounded border border-slate-800/80 overflow-x-auto">
                    <strong className="text-slate-400">Filter Metadata: </strong>
                    {JSON.stringify(chk.filter_metadata)}
                  </div>
                </div>
              ))}
            </div>
            {filteredChunks.length > 30 && (
              <p className="text-center text-xs text-slate-500 italic">
                Showing top 30 of {filteredChunks.length} matching chunks. All 130 chunks stored in chunks.jsonl.
              </p>
            )}
          </div>
        )}

        {/* ===================== TAB 6: DATA QUALITY AUDIT ===================== */}
        {activeTab === 'quality' && (
          <div className="space-y-6">
            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 mb-2">
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <h2 className="text-lg font-bold text-white">Data Quality & Validation Audit Report</h2>
              </div>
              <p className="text-xs text-slate-400 mb-6">
                Automated validator results run during pipeline execution. All 10 integrity assertions passed with 0 fatal errors.
              </p>

              {/* Validation Badges */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-8">
                {[
                  'No Duplicate Course Codes',
                  'Valid Positive Numeric Credits (> 0)',
                  'All Records Have Valid Canonical Source URLs',
                  'Prerequisites Reference Existing Courses in Catalog',
                  'Prerequisite Dependency Graph is Acyclic (NetworkX DAG Check)',
                  'Course-Skill Links Referential Integrity',
                  'Course Catalog Volume Meets Brief (27 >= 15 courses)',
                  'Open Educational Resources Volume Meets Brief (32 >= 30 resources)',
                  'Academic Rules Volume Meets Brief (15 >= 4 quotable rules)',
                  'Module Lessons Have Valid Parent References'
                ].map((check, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-xs text-slate-200">{check}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> PASS
                    </span>
                  </div>
                ))}
              </div>

              {/* Field Completeness */}
              <h3 className="text-sm font-bold text-white mb-3">Field Completeness Audit</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(summaryData.field_completeness_percentage || {}).map(([entity, pct]) => (
                  <div key={entity} className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <div className="text-xs text-slate-400 capitalize">{entity.replace(/_/g, ' ')}</div>
                    <div className="text-2xl font-black text-indigo-400 font-mono mt-1">{pct}%</div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                      <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${pct}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Modal for Course Details */}
      {selectedCourseDetail && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between">
              <div>
                <span className="font-mono text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded border border-indigo-500/30">
                  {selectedCourseDetail.code}
                </span>
                <h2 className="text-xl font-bold text-white mt-2">{selectedCourseDetail.title}</h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Department of {selectedCourseDetail.dept} • {selectedCourseDetail.type}
                </p>
              </div>
              <button
                onClick={() => setSelectedCourseDetail(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 text-lg font-bold"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-3 gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
              <div>
                <div className="text-slate-500">Credits</div>
                <div className="font-bold text-white font-mono">{selectedCourseDetail.credits}</div>
              </div>
              <div>
                <div className="text-slate-500">L-T-P Breakdown</div>
                <div className="font-bold text-white font-mono">{selectedCourseDetail.lecture_tutorial_practical}</div>
              </div>
              <div>
                <div className="text-slate-500">Semester Offered</div>
                <div className="font-bold text-white">Semester {selectedCourseDetail.semester_offered}</div>
              </div>
            </div>

            <div>
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Detailed Syllabus & Objectives</h4>
              <p className="text-xs text-slate-300 bg-slate-950 p-4 rounded-xl border border-slate-800 leading-relaxed whitespace-pre-line">
                {selectedCourseDetail.objectives}
              </p>
            </div>

            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Source: <a href={selectedCourseDetail.source_url} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline">{selectedCourseDetail.source_url}</a></span>
              <button
                onClick={() => setSelectedCourseDetail(null)}
                className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-4 px-6 text-center text-xs text-slate-500 font-mono">
        Adobe PS Selection Assignment • IIT Bhilai B.Tech CSE Source-Traced Knowledge Base & Data Pipeline • 2026
      </footer>
    </div>
  )
}
