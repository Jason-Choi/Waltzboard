import { attributePreferedSignal } from '../controller/attribute';
import { pinnedKeysSignal } from '../controller/dashboard';
import { transformationPreferredSignal } from '../controller/transformation';
import { GleanerChartModel } from '../types/API';
import { ChartView, TitleToken } from '../types/ChartView';

export const toChartView = (chart: GleanerChartModel): ChartView => {
  const specObject = JSON.parse(chart.spec);
  const title = chart.title;
  const titleToken: TitleToken[] = title.map((t) => {
    return {
      text: t,
      isPrefered:
        attributePreferedSignal.peek().includes(t) ||
        transformationPreferredSignal.peek().includes(t.toLowerCase()),
    };
  });
  specObject.autosize = { type: 'fit', contains: 'padding' };
  specObject.title = null;
  if (specObject.encoding && specObject.encoding.color) {
    specObject.encoding.color.legend = { title: null };
  }
  specObject.background = null;

  return {
    key: chart.key,
    spec: specObject,
    statistics: chart.statistics,
    isPinned: pinnedKeysSignal.value.includes(chart.key),
    chartResults: undefined,
    title,
    titleToken,
  };
};
