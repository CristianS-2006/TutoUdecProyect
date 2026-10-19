module.exports = ({ config }) => {
  const projectId =
    process.env.EXPO_PROJECT_ID ||
    config.extra?.eas?.projectId ||
    '1c166824-a032-477e-99ac-c68c273fa6cd';
  const apiUrl =
    process.env.EXPO_PUBLIC_API_URL || config.extra?.apiUrl || null;

  return {
    ...config,
    extra: {
      ...config.extra,
      apiUrl,
      ...(projectId
        ? { eas: { ...config.extra?.eas, projectId } }
        : {}),
    },
  };
};
