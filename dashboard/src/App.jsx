import { useEffect, useMemo, useState } from "react";

import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Code2,
  Database,
  GitBranch,
  GitCommit,
  Layers3,
  RefreshCw,
  ShieldAlert,
  Sparkles,
  TestTube2,
  TrendingUp,
  X,
  Zap,
} from "lucide-react";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  getAnalytics,
  getPipelines,
  getShapAnalytics,
  getPipeline,
} from "./services/api";


/* =========================================================
   HELPERS
========================================================= */

function formatFeatureName(name) {
  return name
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}


function formatDate(dateString) {
  if (!dateString) return "—";

  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) {
    return dateString;
  }

  return date.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}


function getRiskClass(risk) {
  switch (risk?.toUpperCase()) {
    case "LOW":
      return "bg-emerald-50 text-emerald-700 border-emerald-200";

    case "MEDIUM":
      return "bg-amber-50 text-amber-700 border-amber-200";

    case "HIGH":
      return "bg-orange-50 text-orange-700 border-orange-200";

    case "CRITICAL":
      return "bg-red-50 text-red-700 border-red-200";

    default:
      return "bg-slate-50 text-slate-700 border-slate-200";
  }
}


function getRiskBarClass(risk) {
  switch (risk?.toUpperCase()) {
    case "LOW":
      return "bg-emerald-500";

    case "MEDIUM":
      return "bg-amber-500";

    case "HIGH":
      return "bg-orange-500";

    case "CRITICAL":
      return "bg-red-500";

    default:
      return "bg-slate-400";
  }
}


function getProbabilityClass(probability) {
  if (probability >= 80) return "text-red-600";
  if (probability >= 60) return "text-orange-600";
  if (probability >= 30) return "text-amber-600";

  return "text-emerald-600";
}


/* =========================================================
   SMALL COMPONENTS
========================================================= */

function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  iconClass = "bg-indigo-50 text-indigo-600",
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            {title}
          </p>

          <h3 className="text-2xl font-bold text-slate-900 mt-2">
            {value}
          </h3>

          {subtitle && (
            <p className="text-xs text-slate-400 mt-1">
              {subtitle}
            </p>
          )}
        </div>

        <div className={`p-3 rounded-xl ${iconClass}`}>
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
}


function RiskBadge({ risk }) {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${getRiskClass(
        risk
      )}`}
    >
      {risk || "UNKNOWN"}
    </span>
  );
}


function PredictionBadge({ prediction }) {
  const failure = prediction?.toLowerCase() === "failure";

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
        failure
          ? "bg-red-50 text-red-600 border border-red-200"
          : "bg-emerald-50 text-emerald-600 border border-emerald-200"
      }`}
    >
      {failure ? (
        <AlertTriangle size={13} />
      ) : (
        <CheckCircle2 size={13} />
      )}

      {failure ? "Failure" : "Success"}
    </span>
  );
}


function RiskBar({ risk, count, total }) {
  const percentage =
    total > 0 ? Math.round((count / total) * 100) : 0;

  return (
    <div className="mb-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span
            className={`w-2.5 h-2.5 rounded-full ${getRiskBarClass(
              risk
            )}`}
          />

          <span className="text-sm font-medium text-slate-700">
            {risk}
          </span>
        </div>

        <span className="text-sm text-slate-500">
          {count}
        </span>
      </div>

      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${getRiskBarClass(
            risk
          )}`}
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </div>
  );
}


/* =========================================================
   PIPELINE DETAIL DRAWER
========================================================= */

function PipelineDetail({
  pipeline,
  loading,
  onClose,
}) {
  if (!pipeline && !loading) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50">
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-slate-900/15 backdrop-blur-[2px]"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="absolute right-0 top-0 h-full w-[100vw] max-w-none bg-white shadow-2xl overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 z-10 bg-white/95 backdrop-blur border-b border-slate-200 px-6 py-5">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
                  <Activity size={18} />
                </div>

                <div>
                  <p className="text-xs font-medium text-slate-400 uppercase tracking-wide">
                    Pipeline Analysis
                  </p>

                  <h2 className="text-xl font-bold text-slate-900">
                    Pipeline #{pipeline?.id || "—"}
                  </h2>
                </div>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-slate-100 text-slate-500 transition"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {loading ? (
          <div className="p-8">
            <div className="animate-pulse space-y-5">
              <div className="h-32 bg-slate-100 rounded-2xl" />
              <div className="h-24 bg-slate-100 rounded-2xl" />
              <div className="h-80 bg-slate-100 rounded-2xl" />
            </div>
          </div>
        ) : (
          <div className="p-6 space-y-6">

            {/* =================================================
                PREDICTION SUMMARY
            ================================================= */}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm text-slate-500">
                  Prediction
                </p>

                <div className="mt-3">
                  <PredictionBadge
                    prediction={pipeline?.prediction}
                  />
                </div>
              </div>


              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm text-slate-500">
                  Risk Level
                </p>

                <div className="mt-3">
                  <RiskBadge risk={pipeline?.risk_level} />
                </div>
              </div>

            </div>


            {/* =================================================
                PROBABILITY
            ================================================= */}

            <div className="rounded-2xl border border-slate-200 p-5">

              <div className="flex items-center justify-between mb-4">

                <div>
                  <p className="text-sm text-slate-500">
                    Failure Probability
                  </p>

                  <h3
                    className={`text-4xl font-bold mt-1 ${getProbabilityClass(
                      pipeline?.failure_percentage || 0
                    )}`}
                  >
                    {pipeline?.failure_percentage ?? 0}%
                  </h3>
                </div>

                <div className="p-3 rounded-xl bg-indigo-50 text-indigo-600">
                  <TrendingUp size={22} />
                </div>

              </div>


              <div className="h-3 bg-slate-100 rounded-full overflow-hidden">

                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    pipeline?.failure_percentage >= 80
                      ? "bg-red-500"
                      : pipeline?.failure_percentage >= 60
                      ? "bg-orange-500"
                      : pipeline?.failure_percentage >= 30
                      ? "bg-amber-500"
                      : "bg-emerald-500"
                  }`}
                  style={{
                    width: `${Math.min(
                      100,
                      Math.max(
                        0,
                        pipeline?.failure_percentage || 0
                      )
                    )}%`,
                  }}
                />

              </div>

              <div className="flex justify-between mt-2 text-xs text-slate-400">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
              </div>

            </div>


            {/* =================================================
                INPUT FEATURES
            ================================================= */}

            <div>

              <div className="flex items-center gap-2 mb-4">
                <Database
                  size={18}
                  className="text-indigo-600"
                />

                <h3 className="font-bold text-slate-900">
                  Pipeline Features
                </h3>
              </div>


              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">

                {[
                  ["Files Changed", pipeline?.files_changed],
                  ["Lines Added", pipeline?.lines_added],
                  ["Lines Deleted", pipeline?.lines_deleted],
                  ["Previous Failures", pipeline?.previous_failures],
                  ["Previous Runs", pipeline?.previous_runs],
                  [
                    "Historical Failure Rate",
                    pipeline?.historical_failure_rate != null
                      ? `${(
                          pipeline.historical_failure_rate * 100
                        ).toFixed(1)}%`
                      : "—",
                  ],
                  ["Test Count", pipeline?.test_count],
                  ["Test Failures", pipeline?.test_failures],
                  ["Build Duration", `${pipeline?.build_duration ?? "—"}s`],
                  ["Dependency Changes", pipeline?.dependency_changes],
                  ["Commit Frequency", pipeline?.commit_frequency],
                ].map(([label, value]) => (
                  <div
                    key={label}
                    className="border border-slate-200 rounded-xl p-3"
                  >
                    <p className="text-xs text-slate-400">
                      {label}
                    </p>

                    <p className="text-sm font-semibold text-slate-800 mt-1">
                      {value ?? "—"}
                    </p>
                  </div>
                ))}

              </div>

            </div>


            {/* =================================================
                SHAP EXPLANATION
            ================================================= */}

            <div>

              <div className="flex items-center justify-between mb-4">

                <div className="flex items-center gap-2">
                  <Brain
                    size={18}
                    className="text-indigo-600"
                  />

                  <h3 className="font-bold text-slate-900">
                    AI Explanation
                  </h3>
                </div>

                <span className="text-xs text-slate-400">
                  SHAP
                </span>

              </div>


              <div className="space-y-3">

                {(pipeline?.explanation || []).map(
                  (item, index) => {

                    const positive =
                      item.direction ===
                      "increases_failure_risk";

                    const magnitude =
                      Math.min(
                        100,
                        Math.abs(item.impact) * 100
                      );

                    return (
                      <div
                        key={`${item.feature}-${index}`}
                        className="border border-slate-200 rounded-xl p-4"
                      >

                        <div className="flex items-center justify-between gap-4">

                          <div className="min-w-0">

                            <p className="text-sm font-semibold text-slate-800 truncate">
                              {formatFeatureName(
                                item.feature
                              )}
                            </p>

                            <p
                              className={`text-xs mt-1 ${
                                positive
                                  ? "text-red-500"
                                  : "text-emerald-500"
                              }`}
                            >
                              {positive
                                ? "Increases failure risk"
                                : "Decreases failure risk"}
                            </p>

                          </div>


                          <span
                            className={`text-sm font-bold ${
                              positive
                                ? "text-red-600"
                                : "text-emerald-600"
                            }`}
                          >
                            {item.impact > 0 ? "+" : ""}
                            {Number(item.impact).toFixed(3)}
                          </span>

                        </div>


                        <div className="mt-3 h-2 bg-slate-100 rounded-full overflow-hidden">

                          <div
                            className={`h-full rounded-full ${
                              positive
                                ? "bg-red-400"
                                : "bg-emerald-400"
                            }`}
                            style={{
                              width: `${magnitude}%`,
                            }}
                          />

                        </div>

                      </div>
                    );
                  }
                )}

              </div>

            </div>


            {/* =================================================
                TIMESTAMP
            ================================================= */}

            <div className="flex items-center gap-2 text-xs text-slate-400 pt-2">
              <Clock3 size={14} />

              <span>
                Created {formatDate(pipeline?.created_at)}
              </span>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}


/* =========================================================
   MAIN APP
========================================================= */

export default function App() {

  const [analytics, setAnalytics] = useState(null);
  const [pipelines, setPipelines] = useState([]);
  const [shapData, setShapData] = useState([]);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const [error, setError] = useState("");

  const [selectedPipeline, setSelectedPipeline] =
    useState(null);

  const [detailLoading, setDetailLoading] =
    useState(false);


  /* =========================================================
     LOAD DASHBOARD
  ========================================================= */

  async function loadDashboard(showRefreshing = false) {

    try {

      if (showRefreshing) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError("");

      const [
        analyticsResponse,
        pipelinesResponse,
        shapResponse,
      ] = await Promise.all([
        getAnalytics(),
        getPipelines(),
        getShapAnalytics(),
      ]);


      setAnalytics(analyticsResponse);


      if (Array.isArray(pipelinesResponse)) {

        setPipelines(pipelinesResponse);

      } else if (
        Array.isArray(pipelinesResponse?.predictions)
      ) {

        setPipelines(
          pipelinesResponse.predictions
        );

      } else if (
        Array.isArray(pipelinesResponse?.records)
      ) {

        setPipelines(
          pipelinesResponse.records
        );

      } else {

        setPipelines([]);

      }


      if (Array.isArray(shapResponse)) {

        setShapData(shapResponse);

      } else if (
        Array.isArray(shapResponse?.features)
      ) {

        setShapData(
          shapResponse.features
        );

      } else {

        setShapData([]);

      }

    } catch (err) {

      console.error(err);

      setError(
        "Unable to connect to the backend. Make sure FastAPI is running on port 8000."
      );

    } finally {

      setLoading(false);
      setRefreshing(false);

    }
  }


  /* =========================================================
     INITIAL LOAD
  ========================================================= */

  useEffect(() => {

    loadDashboard();

  }, []);


  /* =========================================================
     AUTO REFRESH — 15 SECONDS
  ========================================================= */

  useEffect(() => {

    const interval = setInterval(() => {

      loadDashboard(true);

    }, 15000);

    return () => clearInterval(interval);

  }, []);


  /* =========================================================
     PIPELINE DETAIL
  ========================================================= */

  async function handlePipelineClick(pipeline) {

    setSelectedPipeline(pipeline);
    setDetailLoading(true);

    try {

      const detail = await getPipeline(pipeline.id);

      setSelectedPipeline(detail);

    } catch (err) {

      console.error(
        "Failed to load pipeline detail:",
        err
      );

    } finally {

      setDetailLoading(false);

    }
  }


  /* =========================================================
     DERIVED DATA
  ========================================================= */

  const totalPipelines =
    analytics?.total_pipelines ??
    pipelines.length ??
    0;

  const predictedFailures =
    analytics?.predicted_failures ??
    pipelines.filter(
      (p) =>
        p.prediction?.toLowerCase() ===
        "failure"
    ).length;

  const failureRate =
    analytics?.failure_rate ??
    (totalPipelines > 0
      ? (predictedFailures / totalPipelines) * 100
      : 0);


  const averageProbability =
    analytics?.average_failure_probability ??
    (pipelines.length > 0
      ? pipelines.reduce(
          (sum, p) =>
            sum +
            Number(
              p.failure_percentage ??
                p.failure_probability * 100 ??
                0
            ),
          0
        ) / pipelines.length
      : 0);


  const riskDistribution =
    analytics?.risk_distribution ?? {};


  const highCriticalCount =
    (riskDistribution.HIGH || 0) +
    (riskDistribution.CRITICAL || 0);


  /* =========================================================
     CHART DATA
  ========================================================= */

  const probabilityChartData = useMemo(() => {

    return [...pipelines]
      .sort(
        (a, b) =>
          new Date(a.created_at) -
          new Date(b.created_at)
      )
      .map((pipeline) => ({
        id: pipeline.id,
        name: `#${pipeline.id}`,
        probability: Number(
          pipeline.failure_percentage ??
            Number(
              pipeline.failure_probability ?? 0
            ) * 100
        ),
        risk: pipeline.risk_level,
      }));

  }, [pipelines]);


  /* =========================================================
     RECENT PIPELINES
  ========================================================= */

  const recentPipelines = useMemo(() => {

    return [...pipelines].sort(
      (a, b) =>
        new Date(b.created_at) -
        new Date(a.created_at)
    );

  }, [pipelines]);


  /* =========================================================
     TOP SHAP FACTORS
  ========================================================= */

  const topShapFactors = useMemo(() => {

    return [...shapData]
      .sort(
        (a, b) =>
          Number(b.average_absolute_impact || 0) -
          Number(a.average_absolute_impact || 0)
      )
      .slice(0, 5);

  }, [shapData]);


  /* =========================================================
     LOADING
  ========================================================= */

  if (loading) {

    return (
      <div className="min-h-screen bg-[#f5f7fb] flex items-center justify-center">

        <div className="text-center">

          <div className="w-14 h-14 rounded-2xl bg-indigo-600 text-white flex items-center justify-center mx-auto mb-4 animate-pulse">
            <Brain size={28} />
          </div>

          <h2 className="text-lg font-bold text-slate-800">
            Loading AI Dashboard
          </h2>

          <p className="text-sm text-slate-400 mt-1">
            Connecting to prediction engine...
          </p>

        </div>

      </div>
    );
  }


  /* =========================================================
     ERROR
  ========================================================= */

  if (error) {

    return (
      <div className="min-h-screen bg-[#f5f7fb] flex items-center justify-center p-6">

        <div className="bg-white border border-slate-200 rounded-2xl p-8 max-w-md text-center shadow-sm">

          <div className="w-14 h-14 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center mx-auto mb-4">
            <ShieldAlert size={28} />
          </div>

          <h2 className="text-lg font-bold text-slate-900">
            Backend Unavailable
          </h2>

          <p className="text-sm text-slate-500 mt-2">
            {error}
          </p>

          <button
            onClick={() => loadDashboard()}
            className="mt-5 inline-flex items-center gap-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition"
          >
            <RefreshCw size={16} />
            Retry Connection
          </button>

        </div>

      </div>
    );
  }


  /* =========================================================
     DASHBOARD
  ========================================================= */

  return (
    <div className="min-h-screen bg-[#f5f7fb] text-slate-900">

      <div className="flex min-h-screen">

        {/* =================================================
            SIDEBAR
        ================================================= */}

        <aside className="hidden lg:flex w-64 bg-white border-r border-slate-200 flex-col">

          <div className="p-6 border-b border-slate-100">

            <div className="flex items-center gap-3">

              <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-sm">
                <Brain size={21} />
              </div>

              <div>
                <h1 className="font-bold text-slate-900">
                  CI/CD AI
                </h1>

                <p className="text-xs text-slate-400">
                  Failure Prediction
                </p>
              </div>

            </div>

          </div>


          <nav className="p-4 space-y-1 flex-1">

            <div className="px-3 py-2.5 rounded-xl bg-indigo-50 text-indigo-700 flex items-center gap-3 text-sm font-semibold">
              <Activity size={18} />
              Dashboard
            </div>

            <div className="px-3 py-2.5 rounded-xl text-slate-500 flex items-center gap-3 text-sm">
              <GitBranch size={18} />
              Pipelines
            </div>

            <div className="px-3 py-2.5 rounded-xl text-slate-500 flex items-center gap-3 text-sm">
              <Brain size={18} />
              Model Insights
            </div>

            <div className="px-3 py-2.5 rounded-xl text-slate-500 flex items-center gap-3 text-sm">
              <Database size={18} />
              Data & Analytics
            </div>

          </nav>


          <div className="p-4">

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">

              <div className="flex items-center gap-2 mb-2">
                <Zap
                  size={15}
                  className="text-indigo-600"
                />

                <span className="text-xs font-semibold text-slate-700">
                  AI Engine
                </span>
              </div>

              <p className="text-xs text-slate-400">
                XGBoost prediction engine with SHAP explainability.
              </p>

            </div>

          </div>

        </aside>


        {/* =================================================
            MAIN CONTENT
        ================================================= */}

        <main className="flex-1 min-w-0">

          {/* HEADER */}

          <header className="bg-white border-b border-slate-200 px-5 sm:px-8 py-4">

            <div className="flex items-center justify-between">

              <div>

                <p className="text-xs text-slate-400 font-medium">
                  AI / CI-CD MONITORING
                </p>

                <h2 className="text-xl font-bold text-slate-900 mt-1">
                  Pipeline Intelligence
                </h2>

              </div>


              <button
                onClick={() =>
                  loadDashboard(true)
                }
                disabled={refreshing}
                className="inline-flex items-center gap-2 px-3.5 py-2.5 border border-slate-200 bg-white hover:bg-slate-50 rounded-xl text-sm font-semibold text-slate-700 transition disabled:opacity-60"
              >

                <RefreshCw
                  size={16}
                  className={
                    refreshing
                      ? "animate-spin"
                      : ""
                  }
                />

                <span className="hidden sm:inline">
                  Refresh
                </span>

              </button>

            </div>

          </header>


          <div className="p-5 sm:p-8 space-y-7">


            {/* =================================================
                STATS
            ================================================= */}

            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

              <StatCard
                title="Total Pipelines"
                value={totalPipelines}
                subtitle="Analyzed by AI"
                icon={Layers3}
              />

              <StatCard
                title="Predicted Failures"
                value={predictedFailures}
                subtitle={`${Number(
                  failureRate
                ).toFixed(1)}% failure rate`}
                icon={AlertTriangle}
                iconClass="bg-red-50 text-red-600"
              />

              <StatCard
                title="Avg. Failure Probability"
                value={`${Number(
                  averageProbability
                ).toFixed(1)}%`}
                subtitle="Across analyzed pipelines"
                icon={TrendingUp}
                iconClass="bg-amber-50 text-amber-600"
              />

              <StatCard
                title="High / Critical Risk"
                value={highCriticalCount}
                subtitle="Pipelines needing attention"
                icon={ShieldAlert}
                iconClass="bg-orange-50 text-orange-600"
              />

            </div>


            {/* =================================================
                CHART + RISK
            ================================================= */}

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

              {/* Probability chart */}

              <div className="xl:col-span-2 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

                <div className="flex items-start justify-between mb-6">

                  <div>

                    <div className="flex items-center gap-2">

                      <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
                        <TrendingUp size={17} />
                      </div>

                      <h3 className="font-bold text-slate-900">
                        Failure Probability Trend
                      </h3>

                    </div>

                    <p className="text-xs text-slate-400 mt-2">
                      AI-predicted probability across recent pipelines
                    </p>

                  </div>

                  <span className="text-xs text-slate-400">
                    {pipelines.length} runs
                  </span>

                </div>


                <div className="h-[280px]">

                  {probabilityChartData.length > 0 ? (

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <AreaChart
                        data={probabilityChartData}
                        margin={{
                          top: 10,
                          right: 10,
                          left: -15,
                          bottom: 0,
                        }}
                      >

                        <defs>

                          <linearGradient
                            id="probabilityGradient"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                          >

                            <stop
                              offset="0%"
                              stopColor="#6366f1"
                              stopOpacity={0.25}
                            />

                            <stop
                              offset="100%"
                              stopColor="#6366f1"
                              stopOpacity={0.02}
                            />

                          </linearGradient>

                        </defs>


                        <CartesianGrid
                          strokeDasharray="3 3"
                          vertical={false}
                          stroke="#e2e8f0"
                        />

                        <XAxis
                          dataKey="name"
                          tick={{
                            fontSize: 11,
                            fill: "#94a3b8",
                          }}
                          axisLine={false}
                          tickLine={false}
                        />

                        <YAxis
                          domain={[0, 100]}
                          tickFormatter={(value) =>
                            `${value}%`
                          }
                          tick={{
                            fontSize: 11,
                            fill: "#94a3b8",
                          }}
                          axisLine={false}
                          tickLine={false}
                        />

                        <Tooltip
                          contentStyle={{
                            background: "#ffffff",
                            border:
                              "1px solid #e2e8f0",
                            borderRadius: "12px",
                            boxShadow:
                              "0 10px 30px rgba(15, 23, 42, 0.08)",
                          }}
                          formatter={(value) => [
                            `${Number(value).toFixed(
                              1
                            )}%`,
                            "Failure Probability",
                          ]}
                        />

                        <Area
                          type="monotone"
                          dataKey="probability"
                          stroke="#6366f1"
                          strokeWidth={2.5}
                          fill="url(#probabilityGradient)"
                          activeDot={{
                            r: 6,
                          }}
                        />

                      </AreaChart>

                    </ResponsiveContainer>

                  ) : (

                    <div className="h-full flex items-center justify-center text-sm text-slate-400">
                      No pipeline data available.
                    </div>

                  )}

                </div>

              </div>


              {/* Risk distribution */}

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

                <div className="flex items-center gap-2 mb-2">

                  <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
                    <ShieldAlert size={17} />
                  </div>

                  <h3 className="font-bold text-slate-900">
                    Risk Distribution
                  </h3>

                </div>

                <p className="text-xs text-slate-400 mb-7">
                  Current pipeline risk levels
                </p>


                <RiskBar
                  risk="LOW"
                  count={riskDistribution.LOW || 0}
                  total={totalPipelines}
                />

                <RiskBar
                  risk="MEDIUM"
                  count={riskDistribution.MEDIUM || 0}
                  total={totalPipelines}
                />

                <RiskBar
                  risk="HIGH"
                  count={riskDistribution.HIGH || 0}
                  total={totalPipelines}
                />

                <RiskBar
                  risk="CRITICAL"
                  count={riskDistribution.CRITICAL || 0}
                  total={totalPipelines}
                />

              </div>

            </div>


            {/* =================================================
                RECENT PIPELINES
            ================================================= */}

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

              <div className="px-5 py-5 border-b border-slate-100">

                <div className="flex items-center justify-between">

                  <div>

                    <div className="flex items-center gap-2">

                      <GitBranch
                        size={18}
                        className="text-indigo-600"
                      />

                      <h3 className="font-bold text-slate-900">
                        Recent Pipelines
                      </h3>

                    </div>

                    <p className="text-xs text-slate-400 mt-1">
                      Click a pipeline to view AI analysis
                    </p>

                  </div>

                  <span className="text-xs text-slate-400">
                    Auto-refresh: 15s
                  </span>

                </div>

              </div>


              <div className="divide-y divide-slate-100 max-h-[520px] overflow-y-auto">

                {recentPipelines.length === 0 ? (

                  <div className="p-8 text-center text-sm text-slate-400">
                    No pipelines found.
                  </div>

                ) : (

                  recentPipelines.map((pipeline) => (

                    <button
                      key={pipeline.id}
                      onClick={() =>
                        handlePipelineClick(
                          pipeline
                        )
                      }
                      className="w-full text-left px-5 py-4 hover:bg-slate-50 transition group"
                    >

                      <div className="flex items-center justify-between gap-4">

                        <div className="flex items-center gap-4 min-w-0">

                          <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500 shrink-0">

                            <GitCommit size={18} />

                          </div>


                          <div className="min-w-0">

                            <div className="flex items-center gap-2 flex-wrap">

                              <span className="text-sm font-bold text-slate-800">
                                Pipeline #{pipeline.id}
                              </span>

                              <PredictionBadge
                                prediction={
                                  pipeline.prediction
                                }
                              />

                              <RiskBadge
                                risk={
                                  pipeline.risk_level
                                }
                              />

                            </div>

                            <p className="text-xs text-slate-400 mt-1">
                              {formatDate(
                                pipeline.created_at
                              )}
                            </p>

                          </div>

                        </div>


                        <div className="flex items-center gap-5 shrink-0">

                          <div className="hidden sm:block text-right">

                            <p className="text-xs text-slate-400">
                              Failure probability
                            </p>

                            <p
                              className={`text-sm font-bold mt-1 ${getProbabilityClass(
                                pipeline.failure_percentage ??
                                  pipeline.failure_probability *
                                    100
                              )}`}
                            >
                              {Number(
                                pipeline.failure_percentage ??
                                  pipeline.failure_probability *
                                    100 ??
                                  0
                              ).toFixed(1)}
                              %
                            </p>

                          </div>


                          <ChevronRight
                            size={18}
                            className="text-slate-300 group-hover:text-indigo-500 transition"
                          />

                        </div>

                      </div>

                    </button>

                  ))

                )}

              </div>

            </div>


            {/* =================================================
                MODEL INSIGHTS
            ================================================= */}

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">


              {/* SHAP factors */}

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

                <div className="flex items-center justify-between mb-5">

                  <div>

                    <div className="flex items-center gap-2">

                      <Brain
                        size={18}
                        className="text-indigo-600"
                      />

                      <h3 className="font-bold text-slate-900">
                        Top AI Risk Factors
                      </h3>

                    </div>

                    <p className="text-xs text-slate-400 mt-1">
                      Global SHAP feature importance
                    </p>

                  </div>

                  <Sparkles
                    size={18}
                    className="text-indigo-400"
                  />

                </div>


                <div className="space-y-4">

                  {topShapFactors.length === 0 ? (

                    <p className="text-sm text-slate-400">
                      No SHAP data available.
                    </p>

                  ) : (

                    topShapFactors.map(
                      (factor, index) => {

                        const impact =
                          Number(
                            factor.average_absolute_impact ||
                              0
                          );

                        const width =
                          Math.min(
                            100,
                            impact * 100
                          );

                        return (
                          <div
                            key={factor.feature}
                          >

                            <div className="flex items-center justify-between mb-1.5">

                              <span className="text-sm font-medium text-slate-700">
                                {formatFeatureName(
                                  factor.feature
                                )}
                              </span>

                              <span className="text-xs font-semibold text-slate-500">
                                {impact.toFixed(3)}
                              </span>

                            </div>


                            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">

                              <div
                                className="h-full rounded-full bg-indigo-500"
                                style={{
                                  width: `${width}%`,
                                }}
                              />

                            </div>

                          </div>
                        );
                      }
                    )

                  )}

                </div>

              </div>


              {/* AI Insight */}

              <div className="bg-indigo-600 rounded-2xl p-6 text-white shadow-sm relative overflow-hidden">

                <div className="absolute -right-10 -top-10 w-40 h-40 rounded-full bg-white/10" />
                <div className="absolute -right-20 bottom-0 w-48 h-48 rounded-full bg-white/5" />


                <div className="relative">

                  <div className="flex items-center gap-2 mb-5">

                    <div className="p-2 rounded-lg bg-white/15">
                      <Sparkles size={18} />
                    </div>

                    <span className="font-bold">
                      AI Insight
                    </span>

                  </div>


                  <h3 className="text-xl font-bold leading-snug">
                    {highCriticalCount > 0
                      ? `${highCriticalCount} pipeline${
                          highCriticalCount > 1
                            ? "s"
                            : ""
                        } currently require${
                          highCriticalCount === 1
                            ? "s"
                            : ""
                        } attention.`
                      : "Pipeline health is currently stable."}
                  </h3>


                  <p className="text-indigo-100 text-sm mt-4 leading-relaxed">

                    The prediction engine evaluates historical
                    failure behavior, code changes, testing
                    information, build characteristics and
                    dependency changes to estimate pipeline
                    failure risk.

                  </p>


                  <div className="mt-6 flex flex-wrap gap-2">

                    <span className="px-3 py-1.5 rounded-lg bg-white/10 text-xs font-medium">
                      XGBoost
                    </span>

                    <span className="px-3 py-1.5 rounded-lg bg-white/10 text-xs font-medium">
                      SHAP
                    </span>

                    <span className="px-3 py-1.5 rounded-lg bg-white/10 text-xs font-medium">
                      Real-time API
                    </span>

                  </div>

                </div>

              </div>

            </div>


            {/* FOOTER */}

            <div className="flex items-center justify-between pt-2 text-xs text-slate-400">

              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                Backend connected
              </div>

              <span>
                AI-Based CI/CD Failure Prediction System
              </span>

            </div>

          </div>

        </main>

      </div>


      {/* =====================================================
          DETAIL DRAWER
      ===================================================== */}

      {selectedPipeline && (
        <PipelineDetail
          pipeline={selectedPipeline}
          loading={detailLoading}
          onClose={() =>
            setSelectedPipeline(null)
          }
        />
      )}

    </div>
  );
}